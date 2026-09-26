from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('', include('core.urls')),
]

# I file in media/ (video dei progetti) sono versionati nel repo: li serviamo anche
# in produzione con DEBUG=False. Nota: i file caricati dall'admin su Render finiscono
# su un disco temporaneo e spariscono al deploy successivo -> vanno messi nel repo.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
