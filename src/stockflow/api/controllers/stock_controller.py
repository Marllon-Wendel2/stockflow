from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from stockflow.config.database import SessionLocal
from stockflow.api.views.dtos.stock_dto import StockResponse, StockCreate
from stockflow.api.service.stock_service import (
    create_stock,
    get_all_stocks,
    get_stock_by_id,
    bulk_create_stocks
)

print("🔥 STOCK CONTROLLER LOADED 🔥")

router = APIRouter(prefix="/stocks", tags=["Stocks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=StockResponse)
def register_stock(stock: StockCreate, db: Session = Depends(get_db)):
    return create_stock(db, stock)

@router.get("/", response_model=List[StockResponse])
def list_stocks(db: Session = Depends(get_db)):
    return get_all_stocks(db)

@router.get("/{stock_id}", response_model=StockResponse)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock



@router.post("/bulk", response_model=List[StockResponse])
def ingest_bulk_stocks(
    items: List[StockCreate],
    db: Session = Depends(get_db)
):
    return bulk_create_stocks(db, items)