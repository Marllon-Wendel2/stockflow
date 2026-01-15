from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from stockflow.api.models.stock import Stock
from stockflow.api.models.stock_schema import StockOut
from stockflow.api.views.dtos.stock_dto import StockCreate
from sqlalchemy import func

def create_stock(db: Session, stock: StockCreate):
    db_stock = Stock(**stock.model_dump())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_all_stocks(db: Session):
    return db.query(Stock).all()

def get_stock_by_id(db: Session, stock_id: int):
    return db.query(Stock).filter(Stock.id == stock_id).first()

def bulk_create_stocks(db: Session, items: list[StockCreate]):
    objects = [Stock(**item.model_dump()) for item in items]
    db.add_all(objects)
    db.commit()
    return objects

def get_stock_history_range(
    db: Session,
    start_month: str,
    end_month: str
):
    return (
        db.query(Stock)
        .filter(
            Stock.reference_month >= start_month,
            Stock.reference_month <= end_month
        )
        .all()
    )

def get_month_summary(db: Session, reference_month: str):
    return (
        db.query(
            func.sum(Stock.units_sold).label("total_units_sold"),
            func.sum(Stock.units_sold * Stock.unit_price).label("revenue")
        )
        .filter(Stock.reference_month == reference_month)
        .one()
    )



def register_stock_out(db: Session, payload: StockOut):
    stock = (
        db.query(Stock)
        .filter(Stock.id == payload.product_id)
        .first()
    )

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    if stock.units_in_stock < payload.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Estoque insuficiente"
        )

    stock.units_in_stock -= payload.quantity
    stock.units_sold += payload.quantity

    db.commit()
    db.refresh(stock)

    return stock
