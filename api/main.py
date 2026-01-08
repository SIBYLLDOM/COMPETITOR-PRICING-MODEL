from fastapi import FastAPI, HTTPException
from api.schemas import PricingRequest, PricingResponse
from api.service import get_pricing

app = FastAPI(
    title="Competitor Pricing Model API",
    description="L1-winning pricing recommendation engine (GeM-oriented)",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/pricing/suggest",
    response_model=PricingResponse
)
def suggest_price(payload: PricingRequest):
    result = get_pricing(
        payload.product,
        payload.quantity
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No competitors found for given product"
        )

    return result
