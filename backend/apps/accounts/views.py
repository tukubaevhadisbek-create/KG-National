from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import ProfileSerializer, TelegramAuthRequestSerializer
from .telegram_auth import TelegramAuthError, verify_telegram_init_data

User = get_user_model()


class TelegramAuthView(APIView):
    """
    POST /api/auth/telegram/
    body: {"init_data": "<строка из Telegram.WebApp.initData>"}

    Проверяет подпись Telegram, создаёт User+Profile при первом
    входе (или обновляет данные при повторном), возвращает пару
    JWT токенов access/refresh и профиль.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        request_serializer = TelegramAuthRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        init_data = request_serializer.validated_data["init_data"]

        try:
            parsed = verify_telegram_init_data(init_data)
        except TelegramAuthError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        tg_user = parsed.get("user")
        if not tg_user or "id" not in tg_user:
            return Response(
                {"detail": "Telegram колдонуучусунун маалыматы жок"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        telegram_id = tg_user["id"]

        with transaction.atomic():
            profile, created = Profile.objects.select_for_update().get_or_create(
                telegram_id=telegram_id,
                defaults={
                    "user": User.objects.create(
                        username=f"tg_{telegram_id}",
                    ),
                    "telegram_username": tg_user.get("username", "") or "",
                    "first_name": tg_user.get("first_name", "") or "",
                    "photo_url": tg_user.get("photo_url", "") or "",
                },
            )
            if not created:
                profile.telegram_username = tg_user.get("username", "") or ""
                profile.first_name = tg_user.get("first_name", "") or ""
                profile.photo_url = tg_user.get("photo_url", "") or ""
                profile.save(
                    update_fields=[
                        "telegram_username",
                        "first_name",
                        "photo_url",
                        "updated_at",
                    ]
                )

        refresh = RefreshToken.for_user(profile.user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "profile": ProfileSerializer(profile).data,
                "is_new_user": created,
            },
            status=status.HTTP_200_OK,
        )


class MyProfileView(RetrieveAPIView):
    """GET /api/profile/me/ — профиль текущего авторизованного пользователя."""

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
