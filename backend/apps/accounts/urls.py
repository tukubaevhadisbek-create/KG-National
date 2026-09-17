from django.urls import path

from .dev_views import DevAuthView
from .views import MyProfileView, TelegramAuthView

urlpatterns = [
    path("auth/telegram/", TelegramAuthView.as_view(), name="telegram-auth"),
    # Только для разработки: работает при DEBUG=True и DEV_AUTH_ENABLED=True,
    # иначе отвечает 404 (см. apps/accounts/dev_views.py).
    path("auth/dev/", DevAuthView.as_view(), name="dev-auth"),
    path("profile/me/", MyProfileView.as_view(), name="my-profile"),
]
