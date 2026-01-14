from pydantic import BaseModel

class StockItem(BaseModel):
    reference_month: str
    category: str
    product_name: str
    units_sold: int
    units_in_stock: int
    unit_price: float