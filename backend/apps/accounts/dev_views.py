# -*- coding: utf-8 -*-
"""
Вход БЕЗ Telegram — только для локальной разработки.

Зачем это нужно: настоящий initData можно получить лишь внутри
Telegram-клиента, а фронтенд удобно отлаживать в обычном браузере.
Этот эндпоинт выдаёт JWT по одному telegram_id, без проверки подписи.

Двойная защита, чтобы он никогда не работал в продакшне:
  1) settings.DEBUG должен быть True;
  2) в .env должно быть DEV_AUTH_ENABLED=True.
Если хотя бы одно условие не выполнено — 404, как будто маршрута нет.
"""

import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import ProfileSerializer

User = get_user_model()


def dev_auth_enabled() -> bool:
    flag = os.getenv("DEV_AUTH_ENABLED", "").strip().lower()
    return settings.DEBUG and flag in ("1", "true", "yes", "on")


class DevAuthRequestSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField(min_value=1)
    first_name = serializers.CharField(max_length=128, required=False, default="Азамат")


class DevAuthView(APIView):
    """POST /api/auth/dev/  body: {"telegram_id": 100001, "first_name": "Азамат"}"""

    permission_classes = [AllowAny]

    def post(self, request):
        if not dev_auth_enabled():
            return Response(
                {"detail": "Жок"},
                status=status.HTTP_404_NOT_FOUND,
            )

        request_serializer = DevAuthRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        telegram_id = request_serializer.validated_data["telegram_id"]
        first_name = request_serializer.validated_data["first_name"]

        with transaction.atomic():
            profile = Profile.objects.filter(telegram_id=telegram_id).first()
            if profile is None:
                user = User.objects.create(username=f"tg_{telegram_id}")
                profile = Profile.objects.create(
                    user=user,
                    telegram_id=telegram_id,
                    telegram_username=f"dev_{telegram_id}",
                    first_name=first_name,
                )

        refresh = RefreshToken.for_user(profile.user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "profile": ProfileSerializer(profile).data,
                "is_new_user": False,
            }
        )
