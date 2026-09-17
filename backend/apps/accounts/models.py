from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Профиль игрока (ребёнка). Расширяет стандартного Django User
    игровыми полями: telegram_id, уровень, баланс тыйын.

    ВАЖНО: coins_balance — это ТОЛЬКО кэш для быстрого чтения.
    Источник истины по деньгам — таблица RewardTransaction
    (apps.rewards). Баланс никогда не изменяется напрямую из
    frontend, только через сервисные функции backend'а.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    telegram_username = models.CharField(max_length=64, blank=True, default="")
    first_name = models.CharField(max_length=128, blank=True, default="")
    photo_url = models.URLField(blank=True, default="")

    level = models.PositiveIntegerField(default=1)
    coins_balance = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.first_name or 'Колдонуучу'} ({self.telegram_id})"
