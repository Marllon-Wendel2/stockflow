from stockflow.automation.download.kaggle_downloader import download_pdfs
from stockflow.automation.process.extract_pdf import extract_and_register


def run_automation_pipeline():
    """
    Executa o pipeline completo:
    1. Download dos PDFs
    2. Extração, tratamento e registro na API
    """
    download_pdfs()
    extract_and_register()

    return {
        "status": "success",
        "message": "Pipeline executado com sucesso"
    }
