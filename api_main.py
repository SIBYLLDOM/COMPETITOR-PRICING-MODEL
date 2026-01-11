# api_main.py
"""
FastAPI service for Government Tender L1 Pricing Model
Provides REST API endpoints for pricing predictions
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
import pandas as pd
import json
import os
from datetime import datetime

from filters.competitor_filter import filter_competitors
from processors.seller_average import generate_seller_average
from processors.seller_inflation import enrich_company_check_with_inflation
from processors.seller_l1_price import enrich_with_last_ranked_price
from processors.seller_least_price import enrich_with_least_price
from processors.seller_quantity_analysis import get_quantity_scaling_factor
from processors.seller_final_price import enrich_with_final_price
from processors.l1_price_band import calculate_l1_price_band

# Configuration
RAW_FILE = "data/raw/scraper_single_bid_results_financial.csv"
BASIC_FILE = "data/raw/scraper_single_bid_results_basic.csv"
FILTERED_FILE = "data/processed/filtered_company.csv"
COMPANY_CHECK_FILE = "data/processed/company_check.csv"
MIN_TENDER_PRICE = 50000

# Initialize FastAPI app
app = FastAPI(
    title="L1 Pricing Model API",
    description="Government Tender L1-Optimized Pricing System using Bottom Percentile Learning",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (allow all origins for now - restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# Pydantic Models
# ===========================

class PricingRequest(BaseModel):
    """Request model for L1 pricing prediction"""
    product: str = Field(
        ..., 
        description="Product name or category (e.g., 'Fully Automatic Biochemistry Analyzer')",
        example="3 Part Automated Hematology Analyzer"
    )
    quantity: int = Field(
        ..., 
        gt=0, 
        description="Quantity required (used for context only, not price scaling)",
        example=5
    )
    
    @validator('product')
    def product_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Product name cannot be empty')
        return v.strip()


class PricingResponse(BaseModel):
    """Response model for L1 pricing prediction"""
    product: str
    quantity: int
    low_price: float = Field(..., description="Aggressive L1 floor price (₹)")
    high_price: float = Field(..., description="Conservative L1 ceiling price (₹)")
    price_type: str = Field(default="TOTAL_CONTRACT", description="Price interpretation type")
    confidence: str = Field(..., description="Confidence percentage")
    basis: str = Field(default="filtered_company.csv (L1 percentile pricing)")
    competitors_analyzed: int
    timestamp: str
    warnings: Optional[list] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    data_files_status: Dict[str, bool]


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: str


# ===========================
# Helper Functions
# ===========================

def check_data_files():
    """Check if required data files exist"""
    return {
        "raw_financial": os.path.exists(RAW_FILE),
        "raw_basic": os.path.exists(BASIC_FILE)
    }


def generate_pricing_prediction(product: str, quantity: int) -> Dict[str, Any]:
    """
    Core pricing prediction logic
    Returns pricing recommendation as dictionary
    """
    warnings = []
    
    # Validate data files exist
    if not os.path.exists(RAW_FILE):
        raise FileNotFoundError(f"Financial data file not found: {RAW_FILE}")
    
    # Phase 1: Filter competitors
    try:
        df = pd.read_csv(RAW_FILE, low_memory=False)
        filtered_df = filter_competitors(df, product)
    except Exception as e:
        raise Exception(f"Error filtering competitors: {str(e)}")
    
    if filtered_df.empty:
        raise ValueError(f"No competitors found for product: {product}")
    
    # Save filtered data
    try:
        filtered_df.to_csv(FILTERED_FILE, index=False)
    except PermissionError:
        raise PermissionError(f"Cannot write to {FILTERED_FILE}. File is locked by another process.")
    
    # Phase 2: Generate L1-specific pricing
    try:
        generate_seller_average(FILTERED_FILE, COMPANY_CHECK_FILE)
        enrich_company_check_with_inflation(COMPANY_CHECK_FILE)
        enrich_with_last_ranked_price(FILTERED_FILE, COMPANY_CHECK_FILE)
        enrich_with_least_price(FILTERED_FILE, COMPANY_CHECK_FILE)
    except Exception as e:
        raise Exception(f"Error in L1 pricing calculation: {str(e)}")
    
    # Phase 3: Quantity context (NO rescaling)
    try:
        quantity_factor = get_quantity_scaling_factor(
            BASIC_FILE,
            FILTERED_FILE,
            quantity
        )
        if quantity_factor != 1.0:
            warnings.append(f"Unexpected quantity factor: {quantity_factor} (expected 1.0)")
    except Exception as e:
        warnings.append(f"Quantity analysis failed: {str(e)}. Using neutral factor.")
        quantity_factor = 1.0
    
    # Phase 4: Final price calculation
    try:
        enrich_with_final_price(COMPANY_CHECK_FILE, quantity_factor)
    except Exception as e:
        raise Exception(f"Error calculating final prices: {str(e)}")
    
    # Phase 5: L1 Band calculation
    try:
        low_price, high_price = calculate_l1_price_band(COMPANY_CHECK_FILE)
    except Exception as e:
        raise Exception(f"Error calculating L1 price band: {str(e)}")
    
    # Sanity checks
    if low_price < MIN_TENDER_PRICE or high_price < MIN_TENDER_PRICE:
        warnings.append(f"Price below tender minimum (₹{MIN_TENDER_PRICE:,}). Adjusted to minimum.")
        low_price = max(low_price, MIN_TENDER_PRICE)
        high_price = max(high_price, MIN_TENDER_PRICE)
    
    # Calculate confidence
    df_check = pd.read_csv(COMPANY_CHECK_FILE)
    data_points = len(df_check)
    confidence = min(95, 50 + (data_points * 5))
    
    # Build response
    result = {
        "product": product,
        "quantity": quantity,
        "low_price": round(low_price, 2),
        "high_price": round(high_price, 2),
        "price_type": "TOTAL_CONTRACT",
        "confidence": f"{confidence}%",
        "basis": "filtered_company.csv (L1 percentile pricing)",
        "competitors_analyzed": data_points,
        "timestamp": datetime.now().isoformat(),
        "warnings": warnings if warnings else None
    }
    
    return result


# ===========================
# API Endpoints
# ===========================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "service": "L1 Pricing Model API",
        "version": "2.0.0",
        "status": "online",
        "endpoints": {
            "health": "/health",
            "predict": "/api/v1/predict (POST)",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Verifies API status and data file availability
    """
    data_status = check_data_files()
    
    return {
        "status": "healthy" if all(data_status.values()) else "degraded",
        "timestamp": datetime.now().isoformat(),
        "data_files_status": data_status
    }


@app.post(
    "/api/v1/predict",
    response_model=PricingResponse,
    status_code=status.HTTP_200_OK,
    tags=["Pricing"],
    summary="Get L1 Pricing Prediction",
    description="""
    Generate L1-optimized pricing prediction for government tenders.
    
    **Key Features:**
    - Uses L1-specific learning (bottom 5-10 percentile)
    - Returns TOTAL CONTRACT prices (not unit prices)
    - Quantity is for context only (no price rescaling)
    - Minimum price guardrail: ₹50,000
    
    **Example Request:**
    ```json
    {
        "product": "3 Part Automated Hematology Analyzer",
        "quantity": 5
    }
    ```
    """
)
async def predict_pricing(request: PricingRequest):
    """
    Generate L1 pricing prediction
    
    **Returns:** L1 price band with confidence score and metadata
    """
    try:
        result = generate_pricing_prediction(request.product, request.quantity)
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "No Data Found",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Data File Missing",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "File Lock Error",
                "message": str(e),
                "suggestion": "Close Excel or any program that has output CSV files open",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@app.get("/api/v1/status", tags=["Status"])
async def get_system_status():
    """
    Get detailed system status including configuration
    """
    data_files = check_data_files()
    
    return {
        "service": "L1 Pricing Model",
        "version": "2.0.0",
        "status": "operational",
        "configuration": {
            "min_tender_price": MIN_TENDER_PRICE,
            "price_type": "TOTAL_CONTRACT",
            "learning_method": "L1-specific (bottom 5-10 percentile)",
            "quantity_scaling": "disabled (neutral factor = 1.0)"
        },
        "data_files": {
            "raw_financial": {
                "path": RAW_FILE,
                "exists": data_files["raw_financial"]
            },
            "raw_basic": {
                "path": BASIC_FILE,
                "exists": data_files["raw_basic"]
            }
        },
        "timestamp": datetime.now().isoformat()
    }


# ===========================
# Application Startup/Shutdown
# ===========================

@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    print("\n" + "=" * 70)
    print("🚀 L1 PRICING MODEL API - STARTING")
    print("=" * 70)
    print(f"📊 Version: 2.0.0")
    print(f"🔥 L1-Optimized (Bottom Percentile Learning)")
    print(f"💼 Price Type: TOTAL CONTRACT")
    print(f"📋 Min Tender Price: ₹{MIN_TENDER_PRICE:,}")
    
    # Check data files
    data_status = check_data_files()
    print(f"\n📁 Data Files Status:")
    for filename, exists in data_status.items():
        status_icon = "✅" if exists else "❌"
        print(f"   {status_icon} {filename}: {'Found' if exists else 'Missing'}")
    
    print("\n📚 API Documentation:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")
    print("\n" + "=" * 70)
    print("✅ API READY")
    print("=" * 70 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    print("\n" + "=" * 70)
    print("🛑 L1 PRICING MODEL API - SHUTTING DOWN")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
