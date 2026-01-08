from pydantic import BaseModel, Field
from typing import List


class PricingRequest(BaseModel):
    product: str = Field(
        ...,
        example="HIV ELISA Test Kits"
    )
    quantity: int = Field(
        ...,
        gt=0,
        example=10
    )


class PricingResponse(BaseModel):
    product: str
    quantity: int
    low_price: float
    high_price: float
    top_5_sellers: List[str]
