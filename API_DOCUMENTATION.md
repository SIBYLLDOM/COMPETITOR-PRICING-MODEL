# FastAPI Integration - Complete Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install fastapi uvicorn requests
```

### 2. Start the API Server
```bash
python start_api.py
```

The API will be available at:
- **API Root:** http://localhost:8000
- **Swagger UI (Interactive Docs):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 3. Test the API
```bash
# In a new terminal
python test_api.py
```

---

## 📚 API Endpoints

### 1. Root Endpoint
**GET** `/`

Returns API information and available endpoints.

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
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
```

---

### 2. Health Check
**GET** `/health`

Check API health and data file availability.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-11T10:53:27+05:30",
  "data_files_status": {
    "raw_financial": true,
    "raw_basic": true
  }
}
```

---

### 3. System Status
**GET** `/api/v1/status`

Get detailed system configuration and status.

```bash
curl http://localhost:8000/api/v1/status
```

**Response:**
```json
{
  "service": "L1 Pricing Model",
  "version": "2.0.0",
  "status": "operational",
  "configuration": {
    "min_tender_price": 50000,
    "price_type": "TOTAL_CONTRACT",
    "learning_method": "L1-specific (bottom 5-10 percentile)",
    "quantity_scaling": "disabled (neutral factor = 1.0)"
  },
  "data_files": {
    "raw_financial": {
      "path": "data/raw/scraper_single_bid_results_financial.csv",
      "exists": true
    },
    "raw_basic": {
      "path": "data/raw/scraper_single_bid_results_basic.csv",
      "exists": true
    }
  },
  "timestamp": "2026-01-11T10:53:27+05:30"
}
```

---

### 4. Pricing Prediction (Main Endpoint)
**POST** `/api/v1/predict`

Generate L1-optimized pricing prediction.

#### Request Body

```json
{
  "product": "3 Part Automated Hematology Analyzer",
  "quantity": 5
}
```

#### cURL Example

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product": "3 Part Automated Hematology Analyzer",
    "quantity": 5
  }'
```

#### Python Example

```python
import requests

url = "http://localhost:8000/api/v1/predict"
payload = {
    "product": "3 Part Automated Hematology Analyzer",
    "quantity": 5
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Low Price: ₹{result['low_price']:,.2f}")
print(f"High Price: ₹{result['high_price']:,.2f}")
print(f"Confidence: {result['confidence']}")
```

#### JavaScript Example

```javascript
const url = "http://localhost:8000/api/v1/predict";
const payload = {
  product: "3 Part Automated Hematology Analyzer",
  quantity: 5
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(payload)
})
  .then(response => response.json())
  .then(data => {
    console.log(`Low Price: ₹${data.low_price}`);
    console.log(`High Price: ₹${data.high_price}`);
    console.log(`Confidence: ${data.confidence}`);
  });
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "product": "3 Part Automated Hematology Analyzer",
  "quantity": 5,
  "low_price": 390000,
  "high_price": 410000,
  "price_type": "TOTAL_CONTRACT",
  "confidence": "85%",
  "basis": "filtered_company.csv (L1 percentile pricing)",
  "competitors_analyzed": 10,
  "timestamp": "2026-01-11T10:53:27.123456",
  "warnings": null
}
```

#### Error Responses

**404 Not Found** - No competitors found
```json
{
  "detail": {
    "error": "No Data Found",
    "message": "No competitors found for product: XYZ",
    "timestamp": "2026-01-11T10:53:27.123456"
  }
}
```

**500 Internal Server Error** - File lock error
```json
{
  "detail": {
    "error": "File Lock Error",
    "message": "Cannot write to data/processed/filtered_company.csv",
    "suggestion": "Close Excel or any program that has output CSV files open",
    "timestamp": "2026-01-11T10:53:27.123456"
  }
}
```

**422 Validation Error** - Invalid input
```json
{
  "detail": [
    {
      "loc": ["body", "quantity"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## 🔧 Server Configuration

### Default Configuration
- **Host:** `0.0.0.0` (all network interfaces)
- **Port:** `8000`
- **Auto-reload:** Enabled (development mode)

### Custom Configuration

```bash
# Change port
python start_api.py --port 5000

# Change host (localhost only)
python start_api.py --host 127.0.0.1

# Disable auto-reload (production mode)
python start_api.py --no-reload

# Combined
python start_api.py --host 0.0.0.0 --port 8080 --no-reload
```

---

## 📊 Interactive API Documentation

### Swagger UI
Navigate to http://localhost:8000/docs

Features:
- ✅ Interactive API testing
- ✅ Request/response schemas
- ✅ Try it out functionality
- ✅ Authentication support (if configured)

### ReDoc
Navigate to http://localhost:8000/redoc

Features:
- ✅ Beautiful documentation
- ✅ Searchable
- ✅ Downloadable as HTML
- ✅ Code samples in multiple languages

---

## 🧪 Testing

### Run Test Suite
```bash
python test_api.py
```

### Manual Testing with cURL

**Test 1: Health Check**
```bash
curl http://localhost:8000/health
```

**Test 2: Pricing Prediction**
```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product": "Fully Automatic Biochemistry Analyzer",
    "quantity": 10
  }'
```

**Test 3: Error Handling (Empty Product)**
```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product": "",
    "quantity": 5
  }'
```

### Testing with Postman

1. **Import Collection:**
   - Create new Postman collection
   - Add request: `POST http://localhost:8000/api/v1/predict`
   - Set body to JSON:
     ```json
     {
       "product": "{{product_name}}",
       "quantity": {{quantity}}
     }
     ```

2. **Set Variables:**
   - `product_name`: "3 Part Automated Hematology Analyzer"
   - `quantity`: 5

3. **Send Request**

---

## 🔐 Production Deployment

### Security Considerations

1. **CORS Configuration**
   - Update `allow_origins` in `api_main.py`
   - Restrict to specific domains:
     ```python
     app.add_middleware(
         CORSMiddleware,
         allow_origins=["https://yourdomain.com"],
         allow_credentials=True,
         allow_methods=["GET", "POST"],
         allow_headers=["*"],
     )
     ```

2. **Rate Limiting**
   - Install: `pip install slowapi`
   - Add rate limiting middleware

3. **Authentication**
   - Add API key authentication
   - Use OAuth2 for user authentication

### Deployment Options

#### 1. Using Uvicorn (Production Mode)
```bash
uvicorn api_main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 2. Using Gunicorn + Uvicorn Workers
```bash
pip install gunicorn
gunicorn api_main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### 3. Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t l1-pricing-api .
docker run -p 8000:8000 l1-pricing-api
```

---

## 📋 Request/Response Schema

### Request Schema (PricingRequest)

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| product | string | Yes | Product name or category | "3 Part Automated Hematology Analyzer" |
| quantity | integer | Yes | Quantity (>0) | 5 |

### Response Schema (PricingResponse)

| Field | Type | Description |
|-------|------|-------------|
| product | string | Product name |
| quantity | integer | Requested quantity |
| low_price | float | Aggressive L1 floor (₹) |
| high_price | float | Conservative L1 ceiling (₹) |
| price_type | string | Always "TOTAL_CONTRACT" |
| confidence | string | Confidence percentage |
| basis | string | Data source and method |
| competitors_analyzed | integer | Number of competitors |
| timestamp | string | ISO 8601 timestamp |
| warnings | array | Optional warnings |

---

## ⚡ Performance Tips

1. **File Locks:**
   - Always close CSV files in Excel before API calls
   - Use `check_file_locks.py` to verify

2. **Caching:**
   - For production, implement Redis caching
   - Cache competitor data for frequently requested products

3. **Async Processing:**
   - Current implementation is synchronous
   - Consider async/await for I/O operations

4. **Database:**
   - Consider migrating from CSV to database (PostgreSQL/MongoDB)
   - Faster queries and better concurrency

---

## 🛠️ Troubleshooting

### Issue: "Cannot connect to API"
**Solution:**
```bash
# Check if API is running
curl http://localhost:8000/health

# If not, start it
python start_api.py
```

### Issue: "PermissionError: File is locked"
**Solution:**
```bash
# Close Excel/CSV viewers, then:
python check_file_locks.py

# If files are still locked, identify the process:
# Windows: Use Resource Monitor
# Linux: lsof data/processed/*.csv
```

### Issue: "404 Not Found - No competitors"
**Solution:**
- Check if product name matches data in CSV
- Try broader product names
- Verify `filtered_company.csv` has data

### Issue: "503 Service Unavailable - Data file missing"
**Solution:**
```bash
# Verify data files exist
ls -la data/raw/
ls -la data/processed/

# Check status endpoint
curl http://localhost:8000/api/v1/status
```

---

## 📞 API Support

For issues or questions:
1. Check `/docs` for interactive documentation
2. Run health check: `GET /health`
3. Check system status: `GET /api/v1/status`
4. Review logs in terminal where API is running

---

## ✅ Summary

**To use the FastAPI service:**

1. **Start Server:**
   ```bash
   python start_api.py
   ```

2. **Access Docs:**
   - http://localhost:8000/docs

3. **Make Request:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/predict \
     -H "Content-Type: application/json" \
     -d '{"product": "Your Product", "quantity": 5}'
   ```

4. **Test Suite:**
   ```bash
   python test_api.py
   ```

✅ **Your L1 Pricing Model is now accessible via REST API!**
