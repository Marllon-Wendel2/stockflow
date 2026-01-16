from fastapi import APIRouter

from stockflow.automation.process.pipeline import run_automation_pipeline

router = APIRouter(
    prefix="/automation",
    tags=["Automation"]
)

@router.post(
    "/run",
    summary="Executa pipeline de automação",
    description="""
    Executa a automação completa:
    1. Download de PDFs (Kaggle)
    2. Extração e tratamento
    3. Registro dos dados no sistema
    """
)
def run_automation():
    return run_automation_pipeline()
