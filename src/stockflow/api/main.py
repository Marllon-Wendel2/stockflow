from fastapi import FastAPI
from stockflow.api.views.routes.stock_routes import router as stock_router


app = FastAPI(
    title="StockFlow API",
    version="1.0.0"
)

app.include_router(stock_router)

@app.get("/health")
def health():
    return {"status": "ok"}
