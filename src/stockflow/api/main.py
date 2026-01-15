from fastapi import FastAPI
from stockflow.config.database import engine, Base
from stockflow.api.controllers.stock_controller import router as stock_router

app = FastAPI(
    title="StockFlow API",
    version="1.0.0"
)

app.include_router(stock_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}
