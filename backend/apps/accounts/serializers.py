from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "telegram_id",
            "telegram_username",
            "first_name",
            "photo_url",
            "level",
            "coins_balance",
            "created_at",
        ]
        read_only_fields = fields


class TelegramAuthRequestSerializer(serializers.Serializer):
    """Тело запроса POST /api/auth/telegram/"""

    init_data = serializers.CharField(
        help_text="Строка из window.Telegram.WebApp.initData"
    )
