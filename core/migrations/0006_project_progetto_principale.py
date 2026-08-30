# Generated manually to add the progetto_principale field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_project_video_demo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='progetto_principale',
            field=models.BooleanField(
                default=False,
                help_text='Mostralo come card grande, a parte, sopra la lista progetti (es. il portfolio stesso)',
            ),
        ),
    ]
