import os
from datetime import date

import pytest

# Playwright (API sync) gira dentro un event loop: senza questo Django rifiuta
# le query fatte dai test E2E (es. verificare che il messaggio sia stato salvato).
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

from core.models import (
    Experience, ExperienceHighlight, Formazione, FormazioneHighlight, Project, Skill,
)


@pytest.fixture(autouse=True)
def _static_senza_manifest(settings):
    """In test non esiste staticfiles.json (serve collectstatic): usiamo lo storage
    semplice, così {% static %} funziona anche con DEBUG=False."""
    settings.STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Permette di usare un Chromium già installato (variabile PW_CHROMIUM_EXECUTABLE)."""
    path = os.environ.get("PW_CHROMIUM_EXECUTABLE")
    if path:
        return {**browser_type_launch_args, "executable_path": path}
    return browser_type_launch_args


@pytest.fixture
def skills():
    return {
        "playwright": Skill.objects.create(nome="Playwright", categoria="framework"),
        "cypress": Skill.objects.create(nome="Cypress", categoria="framework"),
        "python": Skill.objects.create(nome="Python", categoria="linguaggio"),
        "gitlab": Skill.objects.create(nome="GitLab CI/CD", categoria="ci_cd"),
    }


@pytest.fixture
def dati_portfolio(skills):
    """Un portfolio minimo ma completo: progetti, esperienze con highlight, formazione."""
    principale = Project.objects.create(
        nome="Restaurant Management System",
        slug="restaurant-management-system",
        descrizione="Sistema full-stack testato a più livelli.",
        repo_url="https://github.com/11292-stella/restaurant-management-system",
        video_demo_url="https://example.com/demo.mp4",
        progetto_principale=True,
    )
    principale.tecnologie.add(skills["playwright"])
    altro = Project.objects.create(
        nome="Cypress E2E", slug="cypress-e2e", descrizione="Suite E2E in Cypress.",
        in_evidenza=True,
    )
    altro.tecnologie.add(skills["cypress"])

    sellogic = Experience.objects.create(
        ruolo="QA Automation Engineer", azienda="Sellogic S.r.l.",
        data_inizio=date(2025, 12, 1), descrizione="Test automation su gestionale web.",
    )
    h1 = ExperienceHighlight.objects.create(
        experience=sellogic, azione="progettazione", area="automation",
        dettaglio="framework E2E con Page Object Model", ordine=0,
    )
    h1.tecnologie.add(skills["cypress"], skills["python"])
    h2 = ExperienceHighlight.objects.create(
        experience=sellogic, azione="costruzione", area="ci_cd",
        dettaglio="pipeline GitLab divisa in job per modulo", ordine=1,
    )
    h2.tecnologie.add(skills["gitlab"], skills["cypress"])

    iliad = Experience.objects.create(
        ruolo="Brand Ambassador", azienda="Iliad",
        data_inizio=date(2024, 10, 1), data_fine=date(2024, 12, 31), descrizione="Stand promozionali.",
    )
    ExperienceHighlight.objects.create(
        experience=iliad, azione="diagnosi", area="altro",
        dettaglio="risoluzione di problematiche hardware sul campo", ordine=0,
    )

    formazione = Formazione.objects.create(
        titolo="Master Full Stack Developer", istituto="Epicode", periodo_label="2025", ordine=0,
    )
    fh = FormazioneHighlight.objects.create(formazione=formazione, testo="Percorso intensivo su", ordine=0)
    fh.tecnologie.add(skills["python"])

    return {"principale": principale, "altro": altro, "sellogic": sellogic, "iliad": iliad}
