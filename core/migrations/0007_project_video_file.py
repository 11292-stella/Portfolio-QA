# Generated manually to add the video_file field (local upload) and update video_demo_url help text

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_project_progetto_principale'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='video_file',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to='project_videos/',
                help_text='Carica qui un video dal tuo computer (mp4/webm consigliati). Se presente, ha priorità sul link qui sopra.',
            ),
        ),
        migrations.AlterField(
            model_name='project',
            name='video_demo_url',
            field=models.URLField(
                blank=True,
                null=True,
                help_text='In alternativa al file: link a un video già online (YouTube, Loom, Vimeo o mp4 diretto)',
            ),
        ),
    ]
