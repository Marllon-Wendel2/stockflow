from fastapi import APIRouter
from stockflow.api.views.dtos.stock_dto import StockItem


router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)

@router.post("/")
def ingest_stock(items: list[StockItem]):
    return items
