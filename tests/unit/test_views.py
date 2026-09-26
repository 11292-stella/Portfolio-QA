import json

import pytest
from django.urls import reverse

from core.models import ContactMessage

pytestmark = pytest.mark.django_db


def test_home_risponde_anche_con_database_vuoto(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    assert "Stella Marucelli" in response.content.decode()


def test_home_mostra_progetti_e_dati_delle_simulazioni(client, dati_portfolio):
    html = client.get(reverse("core:home")).content.decode()
    assert "Restaurant Management System" in html
    assert "Cypress E2E" in html
    assert 'id="sellogic-sim-data"' in html
    assert 'id="iliad-sim-data"' in html
    assert "core/js/home.js" in html


def test_home_elenca_le_skill_per_categoria(client, dati_portfolio):
    response = client.get(reverse("core:home"))
    skills = response.context["skills_by_category"]
    assert skills["Framework / Tool di test"] == ["Cypress", "Playwright"]
    assert "Linguaggio" in skills


def test_dati_simulazione_sellogic_nel_json(client, dati_portfolio):
    response = client.get(reverse("core:home"))
    sim = response.context["sellogic_sim"]
    assert json.dumps(sim)  # serializzabile per json_script
    assert sim["dataset"][0]["dettaglio"] == "framework E2E con Page Object Model"


def test_progetto_principale_escluso_dalla_lista(client, dati_portfolio):
    response = client.get(reverse("core:home"))
    assert dati_portfolio["principale"] not in response.context["progetti"]
    assert response.context["progetto_principale"] == dati_portfolio["principale"]


def test_dettaglio_progetto(client, dati_portfolio):
    url = reverse("core:project_detail", args=["restaurant-management-system"])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["video_embed"] == {"type": "video", "src": "https://example.com/demo.mp4"}
    assert response.context["report_types"] == ["playwright"]


def test_dettaglio_progetto_inesistente_404(client):
    response = client.get(reverse("core:project_detail", args=["non-esiste"]))
    assert response.status_code == 404


def test_contatto_valido_viene_salvato(client):
    response = client.post(reverse("core:contact_create"), {
        "nome": "Recruiter", "email": "hr@example.com", "messaggio": "Ciao Stella, ti va di sentirci?",
    })
    assert response.status_code == 302
    assert response["Location"] == "/#contatti"
    messaggio = ContactMessage.objects.get()
    assert messaggio.email == "hr@example.com"
    assert messaggio.letto is False


@pytest.mark.parametrize("dati", [
    {"nome": "", "email": "hr@example.com", "messaggio": "ciao"},
    {"nome": "Recruiter", "email": "non-una-email", "messaggio": "ciao"},
    {"nome": "Recruiter", "email": "hr@example.com", "messaggio": ""},
])
def test_contatto_non_valido_non_viene_salvato(client, dati):
    response = client.post(reverse("core:contact_create"), dati)
    assert response.status_code == 200
    assert response.context["contact_form"].errors
    assert ContactMessage.objects.count() == 0


def test_get_su_contatti_rimanda_alla_home(client):
    response = client.get(reverse("core:contact_create"))
    assert response.status_code == 302


def test_form_highlight_richiede_login(client, dati_portfolio):
    url = reverse("core:highlight_create", args=[dati_portfolio["sellogic"].id])
    response = client.get(url)
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


def test_file_media_inesistente_404(client):
    assert client.get("/media/project_videos/non-esiste.mp4").status_code == 404


def test_pagina_metodo(client):
    response = client.get(reverse("core:metodo"))
    assert response.status_code == 200
    html = response.content.decode()
    for sezione in ('id="flusso"', 'id="report"', 'id="progress"', 'id="ai"'):
        assert sezione in html
    assert "PROGRESS.md" in html
    assert "Impronto" not in html


def test_home_rimanda_alla_pagina_metodo(client):
    html = client.get(reverse("core:home")).content.decode()
    assert reverse("core:metodo") in html
