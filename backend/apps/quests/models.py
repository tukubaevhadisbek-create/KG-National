from django.db import models

from apps.items.models import Item
from apps.worlds.models import Location


class Quest(models.Model):
    """
    Задание. Для MVP главный тип — FIND_ITEM (игра "Буюмду тап"):
    ребёнку показывают несколько вариантов-предметов (QuestOption),
    из них один правильный (correct_item), нужно указать правильный.
    """

    class QuestType(models.TextChoices):
        FIND_ITEM = "find_item", "Буюмду тап"
        # Остальные типы (үй-бүлө дарагы, атты жабды, боз үй куруу)
        # добавляются на следующих этапах со своей игровой логикой.

    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="quests"
    )
    quest_type = models.CharField(
        max_length=16, choices=QuestType.choices, default=QuestType.FIND_ITEM
    )

    prompt_ky = models.CharField(
        "Тапшырма тексти (кыргызча)",
        max_length=128,
        help_text='Мисалы: "Чыныны тап."',
    )
    correct_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="quests_as_answer"
    )
    reward_coins = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тапшырма"
        verbose_name_plural = "Тапшырмалар"

    def __str__(self):
        return self.prompt_ky


class QuestOption(models.Model):
    """
    Один из вариантов, показываемых ребёнку в задании (включая
    правильный — он тоже должен быть среди QuestOption, чтобы
    порядок отображения полностью контролировался контентом).
    """

    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name="options")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Тапшырманын варианты"
        verbose_name_plural = "Тапшырманын варианттары"
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["quest", "item"], name="unique_quest_item_option"
            )
        ]

    def __str__(self):
        return f"{self.quest} — {self.item}"


class QuestAttempt(models.Model):
    """
    Попытка ответа ребёнка. Хранится для защиты от повторного
    начисления награды и для будущей аналитики/статистики обучения.
    """

    profile = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="quest_attempts"
    )
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name="attempts")
    selected_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    reward_granted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тапшырмага аракет"
        verbose_name_plural = "Тапшырмага аракеттер"
        ordering = ["-created_at"]

    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{self.profile} — {self.quest} {status}"
