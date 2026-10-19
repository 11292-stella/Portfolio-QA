"""Aggiunge al portfolio il progetto "QA Scenari AI", come progetto principale, con il video.

Migrazione di dati: gira da sola al deploy su Render (build.sh esegue migrate),
così il progetto compare senza doverlo inserire a mano dall'admin.
Il video sta negli static del repo (core/static/core/video/), così non sparisce ai deploy.
Se il progetto esiste già (stesso slug) non viene toccato.
"""
from django.db import migrations

SLUG = "qa-scenari-ai"
VIDEO = "/static/core/video/qa-scenari-ai-demo.mp4"

DESCRIZIONE = 'Strumento personale che uso come base per testare i progetti: scrivo un requisito, una regola per riga, scelgo le checklist dell\'area (login, anagrafica, ordini, prodotti, pagamenti, liste) e un modello AI piccolo che gira sul mio computer (Ollama, qwen2.5:3b, gratis e senza API key) restituisce scenari di test in Gherkin italiano, domande aperte per il product owner e scheletri di codice in Playwright, Robot Framework e Appium.\n\nCom\'è nato: volevo un agente AI locale che mi aiutasse a cercare lavoro scrivendo autocandidature su misura per ogni azienda. Ho trovato troppi limiti e l\'ho fermato, ma avevo già Ollama e lo scheletro (risposte in JSON con schema, controlli in Python, ciclo di correzione): l\'ho riusato per qualcosa che mi serve nel lavoro di tutti i giorni.\n\nCome funziona: un punto della checklist alla volta. Passo A, l\'AI sceglie quale riga del requisito parla del punto (0 = nessuna, e allora diventa una domanda aperta invece di un comportamento inventato). Passo B, scrive lo scenario in JSON con schema Pydantic. Python controlla la forma (13 controlli: codice nel Gherkin, testi inventati, livello api scritto come interfaccia, "allora" che si contraddice...) e rimanda gli errori all\'AI, al massimo 3 volte. Gherkin e scheletri li scrive Python, non l\'AI.\n\nMisure: ho confrontato le versioni dei prompt con scenari scritti a mano da me, con ripetizioni e punti instabili come per i test flaky (passo A da 22 a 26 decisioni giuste su 32; una versione che sembrava migliore è stata bocciata con 10 su 32). Il risultato più importante: con le stesse checklist un requisito vago ha dato 4 scenari, lo stesso requisito scritto bene 21. Per questo c\'è anche un controllo del requisito, senza AI, che segnala le righe da migliorare prima dell\'analisi.\n\n24 checklist, 431 punti, interfaccia web in Django. Gli scenari sono una bozza da rivedere: la revisione resta mia.'

TECNOLOGIE = [
    ("Python", "linguaggio"),
    ("Django", "framework"),
    ("Ollama", "altro"),
    ("Pydantic", "altro"),
    ("Gherkin", "altro"),
    ("Playwright", "framework"),
    ("Robot Framework", "framework"),
    ("Appium", "framework"),
]


def aggiungi_progetto(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    Skill = apps.get_model("core", "Skill")
    if Project.objects.filter(slug=SLUG).exists():
        return
    progetto = Project.objects.create(
        nome="QA Scenari AI – dal requisito agli scenari di test",
        slug=SLUG,
        descrizione=DESCRIZIONE,
        repo_url="https://github.com/11292-stella/qa-scenari-ai",
        video_demo_url=VIDEO,
        in_evidenza=True,
        progetto_principale=True,
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
        ("core", "0013_esperienza_progetti_personali"),
    ]

    operations = [
        migrations.RunPython(aggiungi_progetto, rimuovi_progetto),
    ]
