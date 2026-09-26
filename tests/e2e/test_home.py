"""Test end-to-end della home con Playwright su un live server Django."""
import re

import pytest
from playwright.sync_api import Page, expect

from core.models import ContactMessage

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


@pytest.fixture
def home(page: Page, live_server, dati_portfolio) -> Page:
    page.goto(live_server.url + "/")
    return page


def test_navbar_con_cv_e_link_esterni(home: Page, live_server):
    expect(home.get_by_role("link", name="GitHub").first).to_have_attribute(
        "href", "https://github.com/11292-stella"
    )
    expect(home.get_by_role("link", name="LinkedIn")).to_have_attribute(
        "href", re.compile(r"linkedin\.com/in/stella-marucelli")
    )
    cv = home.get_by_role("link", name=re.compile("Scarica CV"))
    href = cv.get_attribute("href")
    assert href.endswith("Stella_Marucelli_CV_v3.pdf")
    # il PDF linkato esiste davvero
    assert home.request.get(live_server.url + href).ok


def test_salta_animazioni_compila_subito_i_form(home: Page):
    skip = home.get_by_role("button", name=re.compile("Salta animazioni"))
    expect(skip).to_be_visible()
    skip.click()

    expect(skip).to_be_hidden()
    expect(home.locator("#ps-ruolo")).to_have_text("QA Automation Engineer & Full Stack Developer")
    expect(home.locator("#ps-bio")).to_contain_text("QA Automation Engineer")
    expect(home.locator("#ps-status")).to_contain_text("presentazione salvata")
    # la simulazione dell'esperienza si ferma sul primo highlight, compilato
    expect(home.locator("#sg-dettaglio")).to_have_text("framework E2E con Page Object Model")
    expect(home.locator("#sg-azione")).to_have_text("Progettazione e sviluppo")


def test_con_animazioni_ridotte_i_form_sono_gia_compilati(browser, live_server, dati_portfolio):
    context = browser.new_context(reduced_motion="reduce")
    page = context.new_page()
    page.goto(live_server.url + "/")
    expect(page.locator("#skip-anim")).to_be_hidden()
    expect(page.locator("#ps-status")).to_contain_text("presentazione salvata")
    context.close()


def test_skill_sempre_leggibili_per_categoria(home: Page):
    gruppi = home.locator(".skills-static-group")
    expect(gruppi).to_have_count(3)
    expect(home.locator(".skills-static")).to_contain_text("Playwright")
    expect(home.locator(".skills-static")).to_contain_text("GitLab CI/CD")


def test_dettagli_del_progetto_principale(home: Page):
    home.locator(".hero-project-card").get_by_role("link", name="Dettagli").click()
    expect(home).to_have_url(re.compile(r"/progetti/restaurant-management-system/$"))
    expect(home.get_by_text("Restaurant Management System").first).to_be_visible()


def test_form_contatti_vuoto_mostra_errori(home: Page):
    home.get_by_role("button", name="Salta animazioni").click()
    home.get_by_role("button", name="Invia messaggio").click()
    expect(home.locator(".site-message-error")).to_contain_text("Controlla i campi")
    assert ContactMessage.objects.count() == 0


def test_form_contatti_valido_salva_il_messaggio(home: Page):
    home.get_by_role("button", name="Salta animazioni").click()
    home.get_by_label("nome").fill("Recruiter Test")
    home.get_by_label("email").fill("recruiter@example.com")
    home.get_by_label("messaggio").fill("Ciao Stella, possiamo sentirci?")
    home.get_by_role("button", name="Invia messaggio").click()

    expect(home.locator(".site-message-success")).to_contain_text("Messaggio inviato")
    messaggio = ContactMessage.objects.get()
    assert messaggio.nome == "Recruiter Test"
