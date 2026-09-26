from django.db import migrations


def rimuovi_nome_piattaforma(apps, schema_editor):
    """Sostituisce il nome della piattaforma aziendale con una descrizione generica
    negli highlight delle esperienze (il portfolio è pubblico)."""
    ExperienceHighlight = apps.get_model('core', 'ExperienceHighlight')
    for h in ExperienceHighlight.objects.filter(dettaglio__icontains='Impronto'):
        h.dettaglio = (
            h.dettaglio
            .replace('la piattaforma gestionale Impronto Enterprise', 'una piattaforma gestionale web per la ristorazione')
            .replace('Impronto Enterprise', 'piattaforma gestionale web')
            .replace('Impronto', 'piattaforma gestionale')
        )
        h.save(update_fields=['dettaglio'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_contactmessage_formazione_formazionehighlight'),
    ]

    operations = [
        migrations.RunPython(rimuovi_nome_piattaforma, migrations.RunPython.noop),
    ]
