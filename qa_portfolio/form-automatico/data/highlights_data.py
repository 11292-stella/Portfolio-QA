HIGHLIGHTS_SELLOGIC = [
    {
        "azione": "Progettazione e sviluppo",
        "area": "Test Automation",
        "tecnologie": ["Cypress", "JavaScript"],
        "dettaglio": "framework di test automation E2E per la piattaforma gestionale Impronto Enterprise, costruito sul Page Object Model con base class condivisa e dati di test dinamici generati con Faker.js (15+ moduli coperti)",
        "ordine": 0,
    },
    {
        "azione": "Progettazione e sviluppo",
        "area": "Test Automation",
        "tecnologie": ["Playwright", "Python"],
        "dettaglio": "stack di automazione E2E complementare con Pytest e Page Object Model, fixture di autenticazione basate su sessione, astrazione BasePage per i pattern UI Vuetify e dati generati con Faker",
        "ordine": 1,
    },
    {
        "azione": "Progettazione e sviluppo",
        "area": "Mobile Testing",
        "tecnologie": ["Appium", "Java", "TestNG"],
        "dettaglio": "suite E2E per un'app Flutter enterprise in produzione, automatizzando flussi multi-schermata e risolvendo blocchi intermittenti di sessione del driver",
        "ordine": 2,
    },
    {
        "azione": "Costruzione e ottimizzazione",
        "area": "CI/CD",
        "tecnologie": ["GitLab CI/CD"],
        "dettaglio": "pipeline con stage install/lint/smoke/test su runner Docker, reporting a doppio formato (Mochawesome/JUnit XML, Allure) e commenti automatici sulle Merge Request",
        "ordine": 3,
    },
    {
        "azione": "Diagnosi e risoluzione",
        "area": "Test Automation",
        "tecnologie": ["Cypress"],
        "dettaglio": "crash del renderer Chrome in ambienti CI headless legati a componenti Vuetify (ResizeObserver/debounce), tramite intercept mirati e trigger di eventi DOM",
        "ordine": 4,
    },
    {
        "azione": "Individuazione e documentazione",
        "area": "Bug Hunting & Security",
        "tecnologie": [],
        "dettaglio": "oltre 50 bug, incluso un payload XSS critico cross-modulo sul sistema POS che eseguiva codice arbitrario sull'interfaccia kiosk",
        "ordine": 5,
    },
]