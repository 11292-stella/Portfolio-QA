"""Aggiunge al portfolio il progetto "Selenium + Cucumber – Gestionale ristorazione", con il video.

Migrazione di dati: gira da sola al deploy su Render (build.sh esegue migrate),
così il progetto compare senza doverlo inserire a mano dall'admin.
Il video sta negli static del repo (core/static/core/video/), così non sparisce ai deploy.
Se il progetto esiste già (stesso slug) non viene toccato.
"""
from django.db import migrations

SLUG = "selenium-cucumber-gestionale"
VIDEO = "/static/core/video/selenium-cucumber-demo.mp4"

DESCRIZIONE = 'Suite E2E web in BDD per il gestionale Angular + Angular Material del Restaurant Management System: 53 scenari scritti in Gherkin italiano (Dato / Quando / Allora) che pilotano Chrome con Selenium 4 su login, categorie e prodotti. Nel video, il report Cucumber dell\'esecuzione completa: 53 scenari su 53 superati.\n\nCome funziona: Page Object Model a tre livelli (BasePage con le attese e gli helper per Angular Material, FormPage con le parti comuni dei form, una pagina per sezione); Cucumber collega ogni frase a step Java e JUnit 5 lancia la suite. Gli scenari entrano già autenticati mettendo il token JWT nel localStorage, preparano i dati via API con REST Assured e verificano ogni operazione due volte: nella UI e nel backend (approccio ibrido UI + API).\n\nCosa copre: CRUD completo di categorie e prodotti, ricerca e filtri combinati (categoria e stato Attivo / Esaurito / Disattivo), validazione dei form (nome vuoto o di soli spazi, prezzo negativo o zero), confirm() del browser accettato e annullato, categoria con prodotti non eliminabile (409), nome già esistente, doppio click su Salva che deve creare un solo prodotto, prezzi formattati in euro, placeholder per i prodotti senza immagine, collegamento tra categorie e prodotti.\n\nSicurezza: nomi con tag HTML (<b>, <img onerror>) devono essere mostrati come testo e non interpretati (XSS).\n\nTecniche: solo attese esplicite con click che riprova sugli elementi "stale" ridisegnati da Angular, selettori XPath per i componenti Material (dropdown, switch, bottoni con icona), DataTable, tag (@smoke, @crud, @validazione, @sicurezza...), dati univoci con Datafaker cancellati a fine scenario anche se il test fallisce, screenshot e HTML della pagina allegati al report sui falliti, configurazione da -D o variabili d\'ambiente pronta per la CI.'

TECNOLOGIE = [
    ("Selenium", "framework"),
    ("Cucumber", "framework"),
    ("Java", "linguaggio"),
    ("JUnit 5", "framework"),
    ("REST Assured", "framework"),
    ("Maven", "altro"),
    ("Angular", "framework"),
]


def aggiungi_progetto(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    Skill = apps.get_model("core", "Skill")
    if Project.objects.filter(slug=SLUG).exists():
        return
    progetto = Project.objects.create(
        nome="Selenium + Cucumber – Gestionale ristorazione (Angular)",
        slug=SLUG,
        descrizione=DESCRIZIONE,
        repo_url="https://github.com/11292-stella/gestionale-selenium-tests",
        video_demo_url=VIDEO,
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
        ("core", "0011_video_appium_cucumber"),
    ]

    operations = [
        migrations.RunPython(aggiungi_progetto, rimuovi_progetto),
    ]
