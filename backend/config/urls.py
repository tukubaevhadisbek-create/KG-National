"""
Главный роутер API.

Все игровые эндпоинты живут под /api/, сгруппированы по приложениям.
Здесь добавлен только один новый блок — apps.assistant.urls
(«Акылдуу жардамчы»), остальное как в исходном файле.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.worlds.urls")),
    path("api/", include("apps.items.urls")),
    path("api/", include("apps.quests.urls")),
    path("api/", include("apps.progress.urls")),
    path("api/", include("apps.achievements.urls")),
    path("api/", include("apps.rooms.urls")),
    path("api/", include("apps.assistant.urls")),

    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
