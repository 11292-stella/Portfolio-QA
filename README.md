# Portfolio QA

[![Test](https://github.com/11292-stella/Portfolio-QA/actions/workflows/tests.yml/badge.svg)](https://github.com/11292-stella/Portfolio-QA/actions/workflows/tests.yml)

Portfolio online che raccoglie report QA, casi di test e progetti di test automation, con video demo. Backend Django con database Postgres dedicato, deployato su Render.

## Cosa contiene

- **Report QA**: report di test strutturati (bug trovati, copertura, esito)
- **Casi di test**: esempi di test case scritti per i progetti mostrati
- **Progetti con video demo**: presentazione dei progetti di automazione (Cypress, Playwright, Appium) con video a corredo

## Stack

- **Backend**: Django
- **Database**: PostgreSQL su Neon in produzione, SQLite in locale
- **Frontend**: template Django + Bootstrap, animazioni in `core/static/core/js/home.js` (dati passati dal database con `json_script`)
- **Test**: pytest + pytest-django (unit/integration) e Playwright (E2E), eseguiti in GitHub Actions
- **Deploy**: Render (build tramite `build.sh`, avvio con `gunicorn qa_portfolio.wsgi:application`)
- **Media**: video dei progetti in `media/project_videos/`

## Struttura del progetto

```
Portfolio-QA/
├── core/                 # app Django principale (modelli, viste, template, static)
├── tests/                # suite di test: unit/ (pytest-django) ed e2e/ (Playwright)
├── .github/workflows/    # CI: esegue tutti i test a ogni push
├── qa_portfolio/         # progetto Django (settings, urls, wsgi)
├── media/project_videos/ # video demo dei progetti mostrati nel portfolio
├── core_data.json        # dati con cui viene popolato il portfolio (report, progetti, ecc.)
├── build.sh              # script di build usato da Render
├── render.yaml           # configurazione del deploy su Render
├── pytest.ini
├── requirements-dev.txt  # dipendenze per i test
├── manage.py
└── requirements.txt
```

## Live

Il portfolio è online su Render, ma il link pubblico è: **[portfolio-loading.vercel.app](https://portfolio-loading.vercel.app/)**

Il piano free di Render "addormenta" il servizio quando resta inattivo: al primo accesso dopo un po' di tempo, il sito reale ci mette diversi secondi a risvegliarsi. Per evitare che chi visita il link pensi a un errore o a un bug, è stata creata una piccola pagina statica (HTML/CSS, stesso stile del portfolio) deployata su Vercel: mostra una schermata di attesa coerente con il design del portfolio mentre il servizio Render si risveglia, poi reindirizza al sito vero.

## Setup in locale

1. Clona il repository e crea un virtual environment.
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. In locale non serve nessuna variabile: senza `DATABASE_URL` Django usa SQLite (`db.sqlite3`). Per vedere gli errori dettagliati avvia in modalità sviluppo:
   ```powershell
   $env:DEBUG="True"
   ```
4. Applica le migration e carica i dati di esempio:
   ```bash
   python manage.py migrate
   python manage.py loaddata core_data.json
   ```
5. Avvia il server di sviluppo:
   ```bash
   python manage.py runserver
   ```

## Test

La suite copre il portfolio stesso, a due livelli:

- **Unit e integration** (`tests/unit`, pytest-django): logica dei video embed (YouTube, Vimeo, Loom, mp4, priorità del file caricato), modelli e dati delle simulazioni, viste (home, dettaglio progetto, 404, form contatti valido e non valido, login richiesto), data migration.
- **End-to-end** (`tests/e2e`, Playwright su live server Django): link della navbar e download del CV, pulsante "Salta animazioni", comportamento con animazioni ridotte, skill leggibili, navigazione al dettaglio progetto, form contatti con errori e con invio riuscito.

```bash
pip install -r requirements-dev.txt
python -m playwright install chromium
pytest            # tutta la suite
pytest tests/unit # solo unit
pytest tests/e2e --headed   # E2E con il browser visibile
```

In CI (GitHub Actions) i test girano a ogni push; report JUnit e trace Playwright dei test falliti vengono salvati come artifact.

> La cartella `qa_portfolio/form-automatico/` contiene invece lo script Playwright che popola gli highlight delle esperienze tramite il form: non fa parte della suite e non viene eseguito da `pytest`.

## Deploy

Il deploy è configurato in `render.yaml`:
- **Web service**: `qa-portfolio`, runtime Python, build con `./build.sh` (install, `collectstatic`, `migrate`), avvio con `gunicorn qa_portfolio.wsgi:application`
- **Variabili d'ambiente**: `DATABASE_URL` (stringa di connessione Neon, impostata a mano), `SECRET_KEY` generata da Render, `DEBUG=False`
- **Media**: i video in `media/` sono versionati nel repo e serviti anche in produzione. I file caricati dall'admin su Render finiscono su un disco temporaneo e spariscono al deploy successivo: vanno aggiunti al repo.
