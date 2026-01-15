from pydantic import BaseModel, Field

class StockOut(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
