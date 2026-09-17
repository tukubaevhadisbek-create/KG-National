from django.conf import settings
from django.db import models


class RewardTransaction(models.Model):
    """
    Журнал (ledger) всех начислений тыйын. Это источник истины по
    деньгам в игре — Profile.coins_balance лишь кэш, посчитанный
    из суммы этих записей сервисным слоем (apps.rewards.services).

    Frontend НИКОГДА не присылает сумму тыйын напрямую — она всегда
    вычисляется на backend (Item.discover_reward, Quest.reward_coins
    и т.д.) и здесь только фиксируется.
    """

    class Reason(models.TextChoices):
        ITEM_DISCOVERED = "item_discovered", "Буюм табылды"
        QUEST_COMPLETED = "quest_completed", "Тапшырма аткарылды"
        BONUS = "bonus", "Бонус"
        FURNITURE_PURCHASE = "furniture_purchase", "Буюм сатылып алынды"

    profile = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="reward_transactions"
    )
    amount = models.IntegerField(help_text="Оң сан — кирешe, терс сан — чыгаша")
    reason = models.CharField(max_length=32, choices=Reason.choices)

    # Универсальная ссылка на источник (например Item id, Quest id),
    # без жёсткой FK-связи, чтобы не тянуть зависимость на все приложения.
    source_type = models.CharField(max_length=32, blank=True, default="")
    source_id = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тыйын транзакциясы"
        verbose_name_plural = "Тыйын транзакциялары"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["profile", "source_type", "source_id"]),
        ]

    def __str__(self):
        return f"{self.profile} — {self.amount} ({self.reason})"
