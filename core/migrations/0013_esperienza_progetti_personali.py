"""Aggiunge l'esperienza "Progetti personali" (2024 — oggi), come nel CV.

Migrazione di dati: gira da sola al deploy su Render (build.sh esegue migrate),
così l'esperienza compare senza doverla inserire a mano dall'admin.
Se esiste già un'esperienza con azienda "Progetti personali" non viene toccata
(si può sempre modificare dall'admin).
"""
import datetime

from django.db import migrations

AZIENDA = "Progetti personali"

DESCRIZIONE = (
    "Applicazioni complete su repository GitHub pubblici, con codice, test automatici e pipeline CI "
    "(dettagli nei progetti qui sotto).\n\n"
    "• Restaurant Management System — backend ASP.NET Core + PostgreSQL, gestionale Angular e kiosk Flutter; "
    "49 test API, 94 test E2E in Robot Framework e 26 scenari BDD mobile in GitLab CI con Docker; "
    "15 bug reali trovati e corretti.\n"
    "• Portfolio QA in Django — questo sito: deploy su Render con Postgres su Neon, testato con pytest-django "
    "e Playwright in GitHub Actions.\n"
    "• Automazione in Python — Job Aggregator e Housing Aggregator: REST API, Gmail API (OAuth2), parsing HTML, "
    "deduplicazione e dashboard su PostgreSQL."
)


def aggiungi_esperienza(apps, schema_editor):
    Experience = apps.get_model("core", "Experience")
    if Experience.objects.filter(azienda__icontains=AZIENDA).exists():
        return
    Experience.objects.create(
        ruolo="Full Stack Developer & Test Automation",
        azienda=AZIENDA,
        data_inizio=datetime.date(2024, 1, 1),
        data_fine=None,  # in corso: in pagina si legge "2024 — oggi"
        descrizione=DESCRIZIONE,
    )


def rimuovi_esperienza(apps, schema_editor):
    apps.get_model("core", "Experience").objects.filter(azienda=AZIENDA).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_progetto_selenium_cucumber"),
    ]

    operations = [
        migrations.RunPython(aggiungi_esperienza, rimuovi_esperienza),
    ]
