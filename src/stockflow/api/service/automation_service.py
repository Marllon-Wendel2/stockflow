import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

AUTOMATION_DIR = BASE_DIR / "automation"

def run_automation_pipeline():
    try:
        # 1️⃣ Download PDFs
        subprocess.run(
            [sys.executable, "kaggle_downloader.py"],
            cwd=AUTOMATION_DIR,
            check=True
        )

        # 2️⃣ Extrair + tratar + registrar na API
        subprocess.run(
            [sys.executable, "extract_pdf.py"],
            cwd=AUTOMATION_DIR,
            check=True
        )

        return {
            "status": "success",
            "message": "Automação executada com sucesso"
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Erro na automação: {str(e)}"
        }
