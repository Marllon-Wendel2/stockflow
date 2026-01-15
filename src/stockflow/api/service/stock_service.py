from sqlalchemy.orm import Session
from stockflow.api.models.stock import Stock
from stockflow.api.views.dtos.stock_dto import StockCreate

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