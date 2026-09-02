from django.contrib import admin

from django.contrib import admin
from .models import (
    Skill, Project, Experience, ExperienceHighlight,
    Formazione, FormazioneHighlight, ContactMessage,
)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'frequenza')
    list_filter = ('categoria',)
    search_fields = ('nome',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('nome', 'in_evidenza', 'progetto_principale', 'stelle_github', 'ultimo_commit')
    list_filter = ('in_evidenza', 'progetto_principale')
    search_fields = ('nome', 'descrizione')
    prepopulated_fields = {'slug': ('nome',)}  # genera lo slug in automatico dal nome mentre digiti
    filter_horizontal = ('tecnologie',)  # UI più comoda per il campo ManyToMany


class ExperienceHighlightInline(admin.TabularInline):
    model = ExperienceHighlight
    extra = 1
    filter_horizontal = ('tecnologie',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('ruolo', 'azienda', 'data_inizio', 'data_fine')
    inlines = [ExperienceHighlightInline]


class FormazioneHighlightInline(admin.TabularInline):
    model = FormazioneHighlight
    extra = 1
    filter_horizontal = ('tecnologie',)


@admin.register(Formazione)
class FormazioneAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'istituto', 'periodo_label', 'ordine')
    list_editable = ('ordine',)
    search_fields = ('titolo', 'istituto')
    inlines = [FormazioneHighlightInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'creato_il', 'letto')
    list_filter = ('letto',)
    list_editable = ('letto',)
    search_fields = ('nome', 'email', 'messaggio')
    readonly_fields = ('nome', 'email', 'messaggio', 'creato_il')
