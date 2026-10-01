import importlib

import pytest
from django.apps import apps

from core.models import ExperienceHighlight
from core.views import build_experience_sim

pytestmark = pytest.mark.django_db


def test_frase_generata_include_azione_dettaglio_e_tecnologie(dati_portfolio):
    h = ExperienceHighlight.objects.get(dettaglio__startswith="framework E2E")
    frase = h.frase_generata()
    assert frase.startswith("Progettazione e sviluppo di framework E2E")
    assert "Cypress" in frase and "Python" in frase


def test_frase_generata_senza_tecnologie(dati_portfolio):
    h = ExperienceHighlight.objects.get(experience=dati_portfolio["iliad"])
    assert h.frase_generata() == "Diagnosi e risoluzione di risoluzione di problematiche hardware sul campo"


def test_simulazione_esperienza_segue_ordine_e_non_duplica_tecnologie(dati_portfolio):
    sim = build_experience_sim(dati_portfolio["sellogic"])
    assert [item["ordine"] for item in sim["dataset"]] == [0, 1]
    assert sim["dataset"][0]["azione"] == "Progettazione e sviluppo"
    assert sim["dataset"][1]["area"] == "CI/CD"
    assert sorted(sim["all_tech"]) == ["Cypress", "GitLab CI/CD", "Python"]


def test_simulazione_senza_esperienza_e_vuota():
    assert build_experience_sim(None) == {"dataset": [], "all_tech": []}


def test_migration_rimuove_nome_piattaforma(dati_portfolio):
    h = ExperienceHighlight.objects.get(dettaglio__startswith="framework E2E")
    h.dettaglio = "framework E2E per la piattaforma gestionale Impronto Enterprise, con POM"
    h.save()

    migration = importlib.import_module("core.migrations.0009_rimuovi_nome_piattaforma_highlight")
    migration.rimuovi_nome_piattaforma(apps, None)

    h.refresh_from_db()
    assert "Impronto" not in h.dettaglio
    assert "una piattaforma gestionale web per la ristorazione" in h.dettaglio


def test_migrazione_aggiunge_il_progetto_appium_cucumber():
    """La migrazione 0010 crea il progetto e collega le tecnologie (senza duplicarle)."""
    import importlib
    from django.apps import apps
    from core.models import Project, Skill

    Skill.objects.create(nome="appium", categoria="framework")   # già esistente, scritta in minuscolo
    migrazione = importlib.import_module("core.migrations.0010_progetto_appium_cucumber")
    migrazione.aggiungi_progetto(apps, None)
    migrazione.aggiungi_progetto(apps, None)                       # seconda volta: non deve duplicare

    progetto = Project.objects.get(slug=migrazione.SLUG)
    assert Project.objects.filter(slug=migrazione.SLUG).count() == 1
    nomi = {t.nome.lower() for t in progetto.tecnologie.all()}
    assert {"appium", "cucumber", "java", "rest assured"} <= nomi
    assert Skill.objects.filter(nome__iexact="appium").count() == 1
