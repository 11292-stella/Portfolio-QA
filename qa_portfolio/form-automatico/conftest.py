import os
import sys
import django
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage

load_dotenv()

# --- setup Django per poter usare i model direttamente da qui ---
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qa_portfolio.settings")
django.setup()

from core.models import ExperienceHighlight

BASE_URL = "http://127.0.0.1:8000"
USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

SELLOGIC_EXPERIENCE_ID = 1


@pytest.fixture(scope="session", autouse=True)
def pulisci_highlight_esistenti():
    """Prima di ogni run della suite, svuota gli highlight di questa esperienza
    così i test ripartono sempre da zero e non si accumulano duplicati."""
    ExperienceHighlight.objects.filter(experience_id=SELLOGIC_EXPERIENCE_ID).delete()


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        pg = context.new_page()

        login_page = LoginPage(pg)
        login_page.vai_a_login(BASE_URL)
        login_page.login(USERNAME, PASSWORD)

        yield pg

        browser.close()