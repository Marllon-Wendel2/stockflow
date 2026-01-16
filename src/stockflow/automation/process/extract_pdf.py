from pathlib import Path
import pdfplumber
import pandas as pd
import re
import requests


def extract_and_register():
    PDF_DIR = Path("/home/marllon/stockflow/data/raw/pdfs")
    OUT_DIR = Path("/home/marllon/stockflow/data/processed/stock_reports")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    row_pattern = re.compile(
        r"""
        ^(?P<category>\w+)\s+
        (?P<product_name>.+?)\s+
        (?P<units_sold>\d+)\s+
        (?P<units_in_stock>\d+)\s+
        (?P<unit_price>\d+(\.\d+)?)
        $
        """,
        re.VERBOSE
    )

    header_pattern = re.compile(r"Stock Report for (\d{4}-\d{2})")

    for pdf_file in sorted(PDF_DIR.glob("*.pdf")):
        print(f"Processando: {pdf_file.name}")

        rows = []

        with pdfplumber.open(pdf_file) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()

        if not text:
            print(f"Texto vazio em {pdf_file.name}")
            continue

        lines = text.split("\n")

        header_match = header_pattern.search(lines[0])
        if not header_match:
            print(f"Cabeçalho não encontrado em {pdf_file.name}")
            continue

        reference_month = header_match.group(1)

        for line in lines[1:]:
            m = row_pattern.match(line)
            if not m:
                continue

            data = m.groupdict()

            rows.append({
                "reference_month": reference_month,
                "category": data["category"],
                "product_name": data["product_name"],
                "units_sold": int(data["units_sold"]),
                "units_in_stock": int(data["units_in_stock"]),
                "unit_price": float(data["unit_price"]),
            })

        if not rows:
            print(f"Nenhuma linha válida em {pdf_file.name}")
            continue

        df = pd.DataFrame(rows)

        df = df[
            (df["units_sold"] >= 0) &
            (df["units_in_stock"] >= 0) &
            (df["unit_price"] > 0)
        ]

        API_URL = "http://stockflow-api:8000/stocks/bulk"

        payload = df.to_dict(orient="records")

        response = requests.post(API_URL, json=payload, timeout=30)

        if response.status_code == 200:
            print(f"Enviado com sucesso: {pdf_file.name}")
        else:
            print(f"Erro ao enviar {pdf_file.name}: {response.status_code}")
            print(response.text)
