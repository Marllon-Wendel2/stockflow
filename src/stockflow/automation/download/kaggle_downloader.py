import os
import requests
from urllib.parse import urlparse
from pathlib import Path
from playwright.sync_api import sync_playwright
from stockflow.config.settings import settings
from src.stockflow.automation.download.auth import auth

DOWNLOAD_DIR = 'data/raw/pdfs'
STATE_PATH = './kaggle_auth.json'
TARGET_URL = 'https://www.kaggle.com/datasets/ayoubcherguelaine/company-documents-dataset'

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_pdfs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        pageAuthenticaded = auth(page)
        
        pageAuthenticaded.goto(TARGET_URL)

        locator = pageAuthenticaded.get_by_text("Data Explorer")
        locator.scroll_into_view_if_needed()
        
        company_documents = pageAuthenticaded.get_by_text("CompanyDocuments")
        company_documents.click()

        invetory_report = pageAuthenticaded.get_by_text("Inventory Report")
        invetory_report.nth(2).click()

        first_monthly = pageAuthenticaded.get_by_text("monthly").nth(0)
        first_monthly.click()

        pageAuthenticaded.wait_for_timeout(800)

        second_monthly = pageAuthenticaded.get_by_text("monthly").nth(1)
        second_monthly.click()

        pageAuthenticaded.wait_for_timeout(800)

        monthly_li = second_monthly.locator("xpath=ancestor::li")

        files_list = monthly_li.locator("ul")
        pdf_items = files_list.get_by_text(".pdf")
        total = pdf_items.count()

        print("PDFs encontrados:", pdf_items.count())

        for i in range(total):
            print(f"Baixando PDF {i + 1}/{total}")

            if(i > 0):
                locator = pageAuthenticaded.get_by_text("Data Explorer")
                locator.scroll_into_view_if_needed()
                
                company_documents = pageAuthenticaded.get_by_text("CompanyDocuments")
                company_documents.click()

                invetory_report = pageAuthenticaded.get_by_text("Inventory Report")
                invetory_report.nth(2).click()

                first_monthly = pageAuthenticaded.get_by_text("monthly").nth(0)
                first_monthly.click()

                pageAuthenticaded.wait_for_timeout(800)

                second_monthly = pageAuthenticaded.get_by_text("monthly").nth(1)
                second_monthly.click()

                pageAuthenticaded.wait_for_timeout(800)

                monthly_li = second_monthly.locator("xpath=ancestor::li")

            monthly_li = pageAuthenticaded.get_by_text("monthly").nth(1).locator("xpath=ancestor::li")
            files_list = monthly_li.locator("ul")
            pdf_items = files_list.get_by_text(".pdf")

            pdf = pdf_items.nth(i)
            pdf.scroll_into_view_if_needed()
            pdf.click()

            download_btn = pageAuthenticaded.get_by_text("get_app")
            download_btn.wait_for(timeout=30000)
            download_btn.click()

            download_url = pageAuthenticaded.url
            filename = os.path.basename(urlparse(download_url).path)
            file_path = os.path.join(DOWNLOAD_DIR, filename)

            if os.path.exists(file_path):
                print(f"Já existe: {filename}")
            else:
                response = requests.get(download_url, timeout=120)
                response.raise_for_status()

                with open(file_path, "wb") as f:
                    f.write(response.content)

                print(f"Baixado: {filename}")

            pageAuthenticaded.go_back()

        pageAuthenticaded.wait_for_timeout(30000)



if __name__ == "__main__":
    print("Iniciando download de PDFs do Kaggle")
    download_pdfs()
    print("Download concluído")