from django.db import models

from apps.worlds.models import Category, Location


class Item(models.Model):
    """
    Интерактивный предмет мира (чыны, комуз, түндүк и т.д.).
    Это ядро всего образовательного контента приложения.
    """

    class Difficulty(models.TextChoices):
        EASY = "easy", "Жеңил"
        MEDIUM = "medium", "Орто"
        HARD = "hard", "Кыйын"

    slug = models.SlugField(unique=True, max_length=64)

    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="items"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="items"
    )

    name_ky = models.CharField("Аталышы (кыргызча)", max_length=64)
    description_ky = models.TextField("Сүрөттөмө (кыргызча)")
    cultural_fact_ky = models.TextField(
        "Маданий факт (кыргызча)", blank=True, default=""
    )

    image = models.ImageField(upload_to="items/", blank=True, null=True)
    audio = models.FileField(upload_to="audio/items/", blank=True, null=True)

    difficulty = models.CharField(
        max_length=8, choices=Difficulty.choices, default=Difficulty.EASY
    )

    # Сколько тыйын начисляется за первое обнаружение этого предмета.
    discover_reward = models.PositiveIntegerField(default=10)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Буюм"
        verbose_name_plural = "Буюмдар"
        ordering = ["location", "category", "name_ky"]

    def __str__(self):
        return self.name_ky
