from django.db import models


class Skill(models.Model):
    CATEGORIA_CHOICES = [
        ('linguaggio', 'Linguaggio'),
        ('framework', 'Framework / Tool di test'),
        ('ci_cd', 'CI/CD'),
        ('database', 'Database / Infrastruttura'),
        ('altro', 'Altro'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='altro')
    # utile se in futuro vuoi calcolare automaticamente quanto "pesa" una skill
    frequenza = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome


class Project(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Usato nell'URL, es: playwright-gestione-catene")
    descrizione = models.TextField()
    repo_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True, help_text="Link al sito/app deployata (se esiste)")
    video_demo_url = models.URLField(
        blank=True, null=True,
        help_text="In alternativa al file: link a un video già online (YouTube, Loom, Vimeo o mp4 diretto)"
    )
    video_file = models.FileField(
        upload_to='project_videos/',
        blank=True, null=True,
        help_text="Carica qui un video dal tuo computer (mp4/webm consigliati). Se presente, ha priorità sul link qui sopra."
    )
    tecnologie = models.ManyToManyField(Skill, blank=True, related_name='progetti')

    stelle_github = models.PositiveIntegerField(default=0)
    ultimo_commit = models.DateTimeField(blank=True, null=True)

    in_evidenza = models.BooleanField(default=False, help_text="Mostralo per primo in home")
    progetto_principale = models.BooleanField(
        default=False,
        help_text="Mostralo come card grande, a parte, sopra la lista progetti (es. il portfolio stesso)"
    )
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Experience(models.Model):
    ruolo = models.CharField(max_length=200)
    azienda = models.CharField(max_length=200)
    data_inizio = models.DateField()
    data_fine = models.DateField(blank=True, null=True, help_text="Lascia vuoto se è il ruolo attuale")
    descrizione = models.TextField()

    def __str__(self):
        return f"{self.ruolo} @ {self.azienda}"

class ExperienceHighlight(models.Model):
    AZIONE_CHOICES = [
        ('progettazione', 'Progettazione e sviluppo'),
        ('diagnosi', 'Diagnosi e risoluzione'),
        ('individuazione', 'Individuazione e documentazione'),
        ('costruzione', 'Costruzione e ottimizzazione'),
        ('audit', 'Audit e revisione'),
        ('redazione', 'Redazione e reportistica'),
        ('studio', 'Studio e implementazione'),
    ]

    AREA_CHOICES = [
        ('automation', 'Test Automation'),
        ('ci_cd', 'CI/CD'),
        ('mobile', 'Mobile Testing'),
        ('bug_hunting', 'Bug Hunting & Security'),
        ('documentazione', 'Documentazione'),
        ('altro', 'Altro'),
    ]

    experience = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name='highlights'
    )
    azione = models.CharField(max_length=20, choices=AZIONE_CHOICES)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    tecnologie = models.ManyToManyField(Skill, blank=True, related_name='highlights')
    dettaglio = models.CharField(
        max_length=300,
        help_text="Il 'cosa': es. 'framework di test E2E in Cypress per la piattaforma Impronto Enterprise'"
    )
    ordine = models.PositiveIntegerField(default=0, help_text="Ordine di visualizzazione (0 = primo)")

    class Meta:
        ordering = ['ordine']

    def frase_generata(self):
        """Genera automaticamente la frase finale combinando i campi."""
        base = f"{self.get_azione_display()} di {self.dettaglio}"
        tech_list = ", ".join(t.nome for t in self.tecnologie.all())
        if tech_list:
            base += f" ({tech_list})"
        return base

    def __str__(self):
        return self.frase_generata()[:80]


class Formazione(models.Model):
    titolo = models.CharField(max_length=200, help_text="Es: Master Full Stack Developer")
    istituto = models.CharField(max_length=200, help_text="Es: Epicode")
    istituto_url = models.URLField(blank=True, null=True, help_text="Link al sito dell'istituto (opzionale)")
    periodo_label = models.CharField(
        max_length=100,
        help_text="Testo libero mostrato in alto a destra. Es: '2025', '2009 — 2011', 'Corso di Formazione'"
    )
    ordine = models.PositiveIntegerField(default=0, help_text="Ordine di visualizzazione (0 = primo)")

    class Meta:
        ordering = ['ordine']
        verbose_name = "Formazione / Certificazione"
        verbose_name_plural = "Formazione & Certificazioni"

    def __str__(self):
        return f"{self.titolo} — {self.istituto}"


class FormazioneHighlight(models.Model):
    formazione = models.ForeignKey(Formazione, on_delete=models.CASCADE, related_name='highlights')
    testo = models.CharField(
        max_length=300,
        help_text="Es: 'Percorso intensivo di programmazione incentrato su' — le tecnologie selezionate sotto verranno aggiunte come tag alla fine della frase."
    )
    tecnologie = models.ManyToManyField(Skill, blank=True, related_name='formazioni_highlights')
    certificazione = models.CharField(
        max_length=200, blank=True,
        help_text="Se compilato, viene mostrato come badge esteso a sé stante (es. 'Epicode Talent - Full Stack Developer'), utile per bullet tipo 'Conseguita certificazione ufficiale'."
    )
    ordine = models.PositiveIntegerField(default=0, help_text="Ordine di visualizzazione (0 = primo)")

    class Meta:
        ordering = ['ordine']

    def __str__(self):
        return self.testo[:80]


class ContactMessage(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField()
    messaggio = models.TextField()
    creato_il = models.DateTimeField(auto_now_add=True)
    letto = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creato_il']

    def __str__(self):
        return f"{self.nome} <{self.email}> — {self.creato_il:%d/%m/%Y %H:%M}"

    # per rimigrare dopo cambiamento: python manage.py makemigrations  python manage.py migrate  python manage.py runserver