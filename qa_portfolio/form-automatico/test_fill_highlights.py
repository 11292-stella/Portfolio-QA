import pytest
from pages.highlight_form_page import HighlightFormPage
from data.highlights_data import HIGHLIGHTS_SELLOGIC

BASE_URL = "http://127.0.0.1:8000"
SELLOGIC_EXPERIENCE_ID = 1  # sostituisci con l'ID reale


@pytest.mark.parametrize("dati_highlight", HIGHLIGHTS_SELLOGIC)
def test_compila_highlight(page, dati_highlight):
    form_page = HighlightFormPage(page)
    form_page.apri_form(BASE_URL, SELLOGIC_EXPERIENCE_ID)
    form_page.compila_e_salva(dati_highlight)

    # verifica che il salvataggio abbia fatto redirect alla home
    page.wait_for_url(f"{BASE_URL}/")