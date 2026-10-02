"""Collega il video dimostrativo al progetto "Appium + Cucumber – Self-Order Kiosk".

Il video sta negli static del repo (core/static/core/video/), così non sparisce
ai deploy su Render come succederebbe a un file caricato dall'admin.
Se dall'admin è già stato impostato un altro video, non viene toccato.
"""
from django.db import migrations

SLUG = "appium-cucumber-self-order-kiosk"
VIDEO = "/static/core/video/appium-cucumber-demo.mp4"


def collega_video(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    progetto = Project.objects.filter(slug=SLUG).first()
    if progetto and not progetto.video_demo_url and not progetto.video_file:
        progetto.video_demo_url = VIDEO
        progetto.save(update_fields=["video_demo_url"])


def scollega_video(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    Project.objects.filter(slug=SLUG, video_demo_url=VIDEO).update(video_demo_url=None)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_progetto_appium_cucumber"),
    ]

    operations = [
        migrations.RunPython(collega_video, scollega_video),
    ]
