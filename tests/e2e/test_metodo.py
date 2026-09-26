"""Test end-to-end della pagina "Metodo" (report case, PROGRESS.md, uso dell'AI)."""
import re

import pytest
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


def test_dalla_navbar_si_apre_la_pagina_metodo(page: Page, live_server):
    page.goto(live_server.url + "/")
    page.get_by_role("link", name="Metodo", exact=True).click()
    expect(page).to_have_url(re.compile(r"/metodo/$"))
    expect(page.get_by_role("heading", level=1)).to_contain_text("il mio metodo QA")


def test_report_case_con_etichette_e_riepilogo(page: Page, live_server):
    page.goto(live_server.url + "/metodo/")
    diario = page.locator("#report-diario")
    expect(diario.locator(".report-item")).to_have_count(6)
    expect(diario.locator(".report-item .tag-bug")).to_have_count(2)
    riepilogo = page.locator("#report-esecutivo .report-table").first
    expect(riepilogo.locator("tbody tr")).to_have_count(5)
    expect(riepilogo).to_contain_text("Critica")


def test_indice_porta_alle_sezioni(page: Page, live_server):
    page.goto(live_server.url + "/metodo/")
    page.get_by_role("navigation", name="Sezioni della pagina").get_by_role("link", name="PROGRESS.md").click()
    expect(page).to_have_url(re.compile(r"#progress$"))
    expect(page.locator("#progress pre")).to_contain_text("## ✅ Fatto")
    expect(page.locator("#ai")).to_contain_text("Il test decide")


def test_banner_in_home_porta_al_metodo(page: Page, live_server, dati_portfolio):
    page.goto(live_server.url + "/")
    banner = page.locator("#metodo-banner")
    expect(banner).to_contain_text("Esplora il mio metodo di lavoro")
    # il banner sta subito dopo il progetto principale, prima della lista progetti
    posizioni = page.evaluate("""() => {
        const y = sel => document.querySelector(sel).getBoundingClientRect().top;
        return [y('.hero-project-card'), y('#metodo-banner'), y('.project-card:not(.hero-project-card)')];
    }""")
    assert posizioni[0] < posizioni[1]
    banner.get_by_text("Scopri il metodo").click()
    expect(page).to_have_url(re.compile(r"/metodo/$"))
