# Portfolio QA

Portfolio online che raccoglie report QA, casi di test e progetti di test automation, con video demo. Backend Django con database Postgres dedicato, deployato su Render.

## Cosa contiene

- **Report QA**: report di test strutturati (bug trovati, copertura, esito)
- **Casi di test**: esempi di test case scritti per i progetti mostrati
- **Progetti con video demo**: presentazione dei progetti di automazione (Cypress, Playwright, Appium) con video a corredo

## Stack

- **Backend**: Django
- **Database**: PostgreSQL (Neon, gestito anche come database Render — vedi `render.yaml`)
- **Deploy**: Render (build tramite `build.sh`, avvio con `gunicorn qa_portfolio.wsgi:application`)
- **Media**: video dei progetti in `media/project_videos/`

## Struttura del progetto

```
Portfolio-QA/
├── core/                 # app Django principale (modelli, viste, template)
├── qa_portfolio/         # progetto Django (settings, urls, wsgi)
├── media/project_videos/ # video demo dei progetti mostrati nel portfolio
├── core_data.json        # dati con cui viene popolato il portfolio (report, progetti, ecc.)
├── build.sh              # script di build usato da Render
├── render.yaml           # configurazione del deploy su Render (web service + database)
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
3. Crea un file `.env` (o configura le variabili d'ambiente) con almeno:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=...
   DEBUG=True
   ```
4. Applica le migration e carica i dati:
   ```bash
   python manage.py migrate
   ```
5. Avvia il server di sviluppo:
   ```bash
   python manage.py runserver
   ```

## Deploy

Il deploy è configurato in `render.yaml`:
- **Database**: `qa-portfolio-db` (piano free)
- **Web service**: `qa-portfolio`, runtime Python, build con `./build.sh`, avvio con `gunicorn qa_portfolio.wsgi:application`
- Variabili d'ambiente collegate automaticamente al database (`DATABASE_URL`), più `SECRET_KEY` generata da Render e `DEBUG=False` in produzione
