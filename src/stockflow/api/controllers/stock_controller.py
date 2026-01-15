from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List

from stockflow.api.models.stock_schema import StockOut
from stockflow.config.database import SessionLocal
from stockflow.api.views.dtos.stock_dto import StockResponse, StockCreate
from stockflow.api.service.stock_service import (
    create_stock,
    get_all_stocks,
    get_stock_by_id,
    bulk_create_stocks,
    get_month_summary,
    get_stock_history_range,
    register_stock_out
)

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    summary="Registrar produto no estoque",
    description="Cria um novo item de estoque para um mês de referência",
    response_model=StockResponse
)
def register_stock(
    stock: StockCreate = Body(...),
    db: Session = Depends(get_db)
):
    return create_stock(db, stock)


@router.get(
    "/",
    summary="Listar todos os produtos",
    response_model=List[StockResponse]
)
def list_stocks(db: Session = Depends(get_db)):
    return get_all_stocks(db)


@router.get(
    "/history",
    summary="Consultar histórico por intervalo de meses",
    description="Retorna produtos cadastrados entre dois meses (YYYY-MM)"
)
def stock_history_range(
    start_month: str = Query(
        ...,
        example="2025-01",
        description="Mês inicial no formato YYYY-MM"
    ),
    end_month: str = Query(
        ...,
        example="2025-02",
        description="Mês final no formato YYYY-MM"
    ),
    db: Session = Depends(get_db)
):
    return get_stock_history_range(db, start_month, end_month)


@router.get(
    "/summary",
    summary="Resumo mensal de estoque",
    description="Retorna total vendido e faturamento do mês"
)
def month_summary(
    reference_month: str = Query(
        ...,
        example="2025-01",
        description="Mês de referência no formato YYYY-MM"
    ),
    db: Session = Depends(get_db)
):
    return get_month_summary(db, reference_month)


@router.get(
    "/{stock_id}",
    summary="Buscar produto por ID",
    response_model=StockResponse
)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = get_stock_by_id(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.post(
    "/bulk",
    summary="Cadastro em massa de produtos",
    description="Registra múltiplos produtos de estoque de uma só vez",
    response_model=List[StockResponse]
)
def ingest_bulk_stocks(
    items: List[StockCreate] = Body(...),
    db: Session = Depends(get_db)
):
    return bulk_create_stocks(db, items)


@router.post(
    "/out",
    summary="Registrar saída de produto",
    description="Registra a saída de unidades de um produto do estoque",
    response_model=StockResponse
)
def stock_out(
    payload: StockOut = Body(...),
    db: Session = Depends(get_db)
):
    return register_stock_out(db, payload)
