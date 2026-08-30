from playwright.sync_api import Page
from .base_page import BasePage


class HighlightFormPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- CAMPI FORM ---
        self.dropdown_azione = page.get_by_label("Azione")
        self.dropdown_area = page.get_by_label("Area")
        self.select_tecnologie = page.get_by_label("Tecnologie")
        self.campo_dettaglio = page.get_by_label("Dettaglio")
        self.campo_ordine = page.get_by_label("Ordine")
        self.btn_salva = page.get_by_role("button", name="Salva highlight")

    # ============================================================
    # NAVIGAZIONE
    # ============================================================

    def apri_form(self, base_url: str, experience_id: int):
        self.page.goto(f"{base_url}/esperienze/{experience_id}/aggiungi-highlight/")
        self.page.wait_for_load_state("load")
    # ============================================================
    # COMPILAZIONE
    # ============================================================
    def compila_e_salva(self, dati_highlight: dict):
        self.dropdown_azione.select_option(label=dati_highlight["azione"])
        self.dropdown_area.select_option(label=dati_highlight["area"])

        for tech in dati_highlight["tecnologie"]:
            self.page.locator(".tech-checks").get_by_text(tech, exact=True).click()

        self.campo_dettaglio.fill(dati_highlight["dettaglio"])
        self.campo_ordine.fill(str(dati_highlight["ordine"]))
        self.btn_salva.click()