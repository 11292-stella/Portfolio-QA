"""Test end-to-end della pagina "Recruiter" (download di CV e scheda candidato)."""
import re

import pytest
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


def test_dalla_navbar_si_apre_la_pagina_recruiter(page: Page, live_server):
    page.goto(live_server.url + "/")
    page.get_by_role("link", name="Recruiter", exact=True).click()
    expect(page).to_have_url(re.compile(r"/recruiter/$"))
    expect(page.get_by_role("heading", level=1)).to_contain_text("candidatura")


def test_tre_file_da_scaricare(page: Page, live_server):
    page.goto(live_server.url + "/recruiter/")
    expect(page.locator("#download .recruiter-dl")).to_have_count(3)
    with page.expect_download() as info:
        page.get_by_role("link", name=re.compile("Scheda candidato")).click()
    assert info.value.suggested_filename == "Scheda_candidato_Stella_Marucelli.pdf"
