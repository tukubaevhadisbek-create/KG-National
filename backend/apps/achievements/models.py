from django.db import models


class Achievement(models.Model):
    """
    Достижение — экран "Менин жетишкендиктерим".
    Условие открытия задаётся декларативно: condition_type указывает,
    какой счётчик из UserProgress проверять, threshold — при каком
    значении достижение считается открытым. Это позволяет добавлять
    новые достижения из Django Admin, без изменения кода.
    """

    class ConditionType(models.TextChoices):
        ITEMS_FOUND = "items_found", "Табылган буюмдардын саны"
        QUESTS_COMPLETED = "quests_completed", "Аяктаган тапшырмалардын саны"
        WORDS_LEARNED = "words_learned", "Үйрөнгөн сөздөрдүн саны"
        CORRECT_ANSWERS = "correct_answers", "Туура жооптордун саны"

    slug = models.SlugField(unique=True, max_length=64)
    title_ky = models.CharField("Аталышы (кыргызча)", max_length=64)
    description_ky = models.CharField("Сүрөттөмө (кыргызча)", max_length=160)
    icon = models.ImageField(upload_to="rewards/achievements/", blank=True, null=True)

    condition_type = models.CharField(max_length=32, choices=ConditionType.choices)
    threshold = models.PositiveIntegerField(
        help_text="Мисалы: 10 (10 сөз үйрөнгөндө ачылат)"
    )

    reward_coins = models.PositiveIntegerField(
        default=0, help_text="Ачылганда кошумча берилүүчү тыйын (милдеттүү эмес)"
    )
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Жетишкендик"
        verbose_name_plural = "Жетишкендиктер"
        ordering = ["order", "threshold"]

    def __str__(self):
        return self.title_ky


class UserAchievement(models.Model):
    """Факт того, что конкретный ребёнок открыл конкретное достижение."""

    profile = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="unlocked_achievements"
    )
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, related_name="unlocked_by"
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ачылган жетишкендик"
        verbose_name_plural = "Ачылган жетишкендиктер"
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "achievement"], name="unique_profile_achievement"
            )
        ]
        ordering = ["-unlocked_at"]

    def __str__(self):
        return f"{self.profile} → {self.achievement}"
