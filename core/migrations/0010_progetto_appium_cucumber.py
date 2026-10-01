"""Aggiunge al portfolio il progetto "Appium + Cucumber – Self-Order Kiosk".

Migrazione di dati: gira da sola al deploy su Render (build.sh esegue migrate),
così il progetto compare senza doverlo inserire a mano dall'admin.
Se esiste già (stesso slug) non viene toccato.
"""
from django.db import migrations

SLUG = "appium-cucumber-self-order-kiosk"

DESCRIZIONE = 'Suite E2E mobile in BDD per il kiosk self-order Flutter del Restaurant Management System: 26 scenari di regressione scritti in Gherkin italiano (Dato / Quando / Allora) che pilotano l\'app vera su emulatore Android come farebbe un cliente, dalla splash all\'ordine confermato.\n\nCome funziona: Appium con il driver Flutter Integration trova i widget tramite le Key Flutter; Cucumber collega ogni frase dello scenario a step Java che usano Page Object (una classe per schermata). Ogni ordine fatto dall\'app viene poi verificato nel backend con REST Assured: cliente, prodotti, quantità, prezzo di listino e totale (approccio ibrido UI + API).\n\nCosa copre: flusso completo di ordine, quantità e totali del carrello, regola "stesso prodotto due volte", validazione del nome (vuoto, solo spazi, apostrofi e accenti), filtro per categoria, limiti della quantità, doppio tocco su "Conferma" (un solo ordine), ritorno automatico al menu. Scenario Outline con i dati in tabella, Datafaker, tag @smoke / @regressione / @api / @bug, attese su condizione (niente sleep), report Cucumber HTML, JUnit e Allure.\n\nBug trovati: le note scritte dal cliente non arrivano al backend; l\'API dell\'ordine espone il costo di produzione all\'app pubblica (OWASP API, excessive data exposure); il menu non si aggiorna mai durante la giornata; il filtro categoria resta al cliente successivo. I bug noti sono documentati da scenari @bug che falliscono finché non vengono corretti.\n\nNel repo c\'è anche CHECKLIST_MOBILE.md: la guida che uso per testare un\'app mobile senza avere il codice sorgente.'

TECNOLOGIE = [
    ("Appium", "framework"),
    ("Cucumber", "framework"),
    ("Java", "linguaggio"),
    ("TestNG", "framework"),
    ("REST Assured", "framework"),
    ("Flutter", "framework"),
    ("Allure", "altro"),
]


def aggiungi_progetto(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    Skill = apps.get_model("core", "Skill")
    if Project.objects.filter(slug=SLUG).exists():
        return
    progetto = Project.objects.create(
        nome="Appium + Cucumber – Self-Order Kiosk (Flutter)",
        slug=SLUG,
        descrizione=DESCRIZIONE,
        repo_url="https://github.com/11292-stella/self-order-kiosk-test-cucumber",
        in_evidenza=True,
    )
    for nome, categoria in TECNOLOGIE:
        skill = Skill.objects.filter(nome__iexact=nome).first()
        if skill is None:
            skill = Skill.objects.create(nome=nome, categoria=categoria)
        progetto.tecnologie.add(skill)


def rimuovi_progetto(apps, schema_editor):
    apps.get_model("core", "Project").objects.filter(slug=SLUG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_rimuovi_nome_piattaforma_highlight"),
    ]

    operations = [
        migrations.RunPython(aggiungi_progetto, rimuovi_progetto),
    ]
