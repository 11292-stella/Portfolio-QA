# Generated manually to add the video_demo_url field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_experiencehighlight'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='video_demo_url',
            field=models.URLField(
                blank=True,
                null=True,
                help_text='Link a un breve video dimostrativo del progetto (YouTube, Loom, Vimeo o file .mp4 diretto)',
            ),
        ),
    ]
