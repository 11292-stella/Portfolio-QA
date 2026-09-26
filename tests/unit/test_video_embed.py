import pytest

from core.models import Project
from core.views import build_video_embed


def progetto(**campi):
    # istanza non salvata: build_video_embed legge solo gli attributi
    return Project(nome="p", slug="p", descrizione="d", **campi)


def test_nessun_progetto_ritorna_none():
    assert build_video_embed(None) is None


def test_progetto_senza_video_ritorna_none():
    assert build_video_embed(progetto()) is None


@pytest.mark.parametrize("url, atteso", [
    ("https://www.youtube.com/watch?v=abc123", "https://www.youtube.com/embed/abc123"),
    ("https://youtu.be/abc123", "https://www.youtube.com/embed/abc123"),
    ("https://vimeo.com/987654", "https://player.vimeo.com/video/987654"),
    ("https://www.loom.com/share/xyz789", "https://www.loom.com/embed/xyz789"),
])
def test_link_esterni_diventano_iframe(url, atteso):
    embed = build_video_embed(progetto(video_demo_url=url))
    assert embed == {"type": "iframe", "src": atteso}


@pytest.mark.parametrize("url", [
    "https://example.com/demo.mp4",
    "https://example.com/demo.WEBM",
    "https://example.com/demo.mov?v=2",
])
def test_file_video_diretti_usano_il_player(url):
    assert build_video_embed(progetto(video_demo_url=url)) == {"type": "video", "src": url}


def test_url_sconosciuto_fallback_iframe():
    embed = build_video_embed(progetto(video_demo_url="https://example.com/pagina"))
    assert embed["type"] == "iframe"


def test_file_caricato_ha_priorita_sul_link():
    p = progetto(video_demo_url="https://youtu.be/abc123")
    p.video_file.name = "project_videos/demo.mp4"
    embed = build_video_embed(p)
    assert embed["type"] == "video"
    assert embed["src"].endswith("project_videos/demo.mp4")
