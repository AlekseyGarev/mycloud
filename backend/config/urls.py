from pathlib import Path
from django.conf import settings
from django.contrib import admin
from django.http import FileResponse, HttpResponse
from django.urls import include, path, re_path


def spa_view(request):
    index_file = Path(settings.FRONTEND_DIST) / 'index.html'
    if not index_file.exists():
        return HttpResponse(
            'Frontend не собран. Выполните npm ci && npm run build в папке frontend.',
            status=503,
            content_type='text/plain; charset=utf-8',
        )
    return FileResponse(index_file.open('rb'), content_type='text/html')


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('storage.urls')),
    path('', spa_view, name='spa-index'),
    re_path(r'^(?!api/|django-admin/|static/|media/).*$', spa_view, name='spa-fallback'),
]
