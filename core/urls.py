from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('progetti/<slug:slug>/', views.project_detail, name='project_detail'),
    path('esperienze/<int:experience_id>/aggiungi-highlight/', views.highlight_create, name='highlight_create'),
    path('contatti/invia/', views.contact_create, name='contact_create'),
]