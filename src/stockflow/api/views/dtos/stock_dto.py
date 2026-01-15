from pydantic import BaseModel
from typing import Optional


class StockBase(BaseModel):
    reference_month: str
    category: str
    product_name: str
    units_sold: int
    units_in_stock: int
    unit_price: float


class StockCreate(StockBase):
    pass


class StockResponse(StockBase):
    id: int

    class Config:
        from_attributes = True
