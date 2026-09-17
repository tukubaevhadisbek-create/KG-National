from django.db import models

from apps.items.models import Item


class UserProgress(models.Model):
    """
    Агрегированный прогресс профиля. Числа здесь — денормализованный
    кэш (для быстрого экрана "Менин жетишкендиктерим"); настоящие
    данные лежат в DiscoveredItem и apps.quests.QuestAttempt.
    """

    profile = models.OneToOneField(
        "accounts.Profile", on_delete=models.CASCADE, related_name="progress"
    )

    words_learned_count = models.PositiveIntegerField(default=0)
    items_found_count = models.PositiveIntegerField(default=0)
    quests_completed_count = models.PositiveIntegerField(default=0)
    correct_answers_count = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Колдонуучунун прогресси"
        verbose_name_plural = "Колдонуучулардын прогресстери"

    def __str__(self):
        return f"Прогресс: {self.profile}"


class DiscoveredItem(models.Model):
    """Факт того, что конкретный ребёнок уже открыл конкретный предмет."""

    profile = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="discovered_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="discovered_by")
    discovered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Табылган буюм"
        verbose_name_plural = "Табылган буюмдар"
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "item"], name="unique_profile_item_discovery"
            )
        ]

    def __str__(self):
        return f"{self.profile} → {self.item}"
