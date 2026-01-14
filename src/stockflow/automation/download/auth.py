from playwright.sync_api import sync_playwright
from stockflow.config.settings import settings

AUTH_FILE = "kaggle_auth.json"

def auth(page):
    page.goto(settings.kaggle_dataset_login)

    page.fill('input[name="email"]', settings.login_email)
    page.fill('input[name="password"]', settings.password)
    page.click('button[type="submit"]')

    page.wait_for_timeout(2000)

    return page

if __name__ == "__main__":
    auth()
