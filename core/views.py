import re

from django.shortcuts import render, get_object_or_404
from .models import Project, Skill, Experience
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Project, Skill, Experience, ExperienceHighlight
from .forms import ExperienceHighlightForm


def build_video_embed(progetto):
    """Prepara i dati per l'embed video: priorità al file caricato, poi al link esterno."""
    if not progetto:
        return None

    if progetto.video_file:
        return {'type': 'video', 'src': progetto.video_file.url}

    url = progetto.video_demo_url
    if not url:
        return None

    youtube_match = re.search(
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w-]+)', url
    )
    if youtube_match:
        return {'type': 'iframe', 'src': f'https://www.youtube.com/embed/{youtube_match.group(1)}'}

    vimeo_match = re.search(r'vimeo\.com/(?:video/)?(\d+)', url)
    if vimeo_match:
        return {'type': 'iframe', 'src': f'https://player.vimeo.com/video/{vimeo_match.group(1)}'}

    loom_match = re.search(r'loom\.com/(?:share|embed)/([\w-]+)', url)
    if loom_match:
        return {'type': 'iframe', 'src': f'https://www.loom.com/embed/{loom_match.group(1)}'}

    if re.search(r'\.(mp4|webm|mov)(\?.*)?$', url, re.IGNORECASE):
        return {'type': 'video', 'src': url}

    # fallback: prova comunque in iframe
    return {'type': 'iframe', 'src': url}


def home(request):
    progetto_principale = Project.objects.filter(progetto_principale=True).first()
    progetti = Project.objects.exclude(pk=getattr(progetto_principale, 'pk', None)).order_by('-in_evidenza', '-data_creazione')
    skills = Skill.objects.all().order_by('categoria', 'nome')

    skills_by_category = {}
    for s in skills:
        skills_by_category.setdefault(s.get_categoria_display(), []).append(s.nome)

    exp_sellogic = Experience.objects.filter(azienda__icontains='Sellogic').first()
    exp_iliad = Experience.objects.filter(azienda__icontains='Iliad').first()

    sellogic_tech = []
    if exp_sellogic:
        sellogic_tech = Skill.objects.filter(
            highlights__experience=exp_sellogic
        ).distinct().order_by('nome')

    principale_video = build_video_embed(progetto_principale)

    context = {
        'progetto_principale': progetto_principale,
        'principale_video': principale_video,
        'progetti': progetti,
        'skills_by_category': skills_by_category,
        'exp_sellogic': exp_sellogic,
        'exp_iliad': exp_iliad,
        'sellogic_tech': sellogic_tech,
    }
    return render(request, 'core/home.html', context)


def project_detail(request, slug):
    progetto = get_object_or_404(Project, slug=slug)

    tech_names = set(t.nome.lower() for t in progetto.tecnologie.all())
    report_types = []
    if 'cypress' in tech_names:
        report_types.append('cypress')
    if 'playwright' in tech_names:
        report_types.append('playwright')
    if 'appium' in tech_names:
        report_types.append('appium')

    video_embed = build_video_embed(progetto)

    context = {'progetto': progetto, 'report_types': report_types, 'video_embed': video_embed}
    return render(request, 'core/project_detail.html', context)

@login_required
def highlight_create(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)

    if request.method == 'POST':
        form = ExperienceHighlightForm(request.POST)
        if form.is_valid():
            highlight = form.save(commit=False)
            highlight.experience = experience
            highlight.save()
            form.save_m2m()  # necessario per salvare il campo ManyToMany (tecnologie)
            return redirect('core:home')
    else:
        form = ExperienceHighlightForm()

    context = {'form': form, 'experience': experience}
    return render(request, 'core/highlight_form.html', context)