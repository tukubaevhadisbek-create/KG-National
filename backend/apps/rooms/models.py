from django.db import models


class Furniture(models.Model):
    """
    Каталог мебели/предметов для кастомизации комнаты (раздел 8 ТЗ):
    стол, отургуч, төшөк, килем, шырдак, сандык, кийим, жасалга и т.д.
    Покупается за тыйын через apps.rooms.services.purchase_furniture.
    """

    class RoomItemCategory(models.TextChoices):
        TABLE = "table", "Үстөл"
        CHAIR = "chair", "Отургуч"
        BED = "bed", "Төшөк"
        CARPET = "carpet", "Килем"
        SHYRDAK = "shyrdak", "Шырдак"
        CHEST = "chest", "Сандык"
        CLOTHING = "clothing", "Улуттук кийим"
        DECOR = "decor", "Жасалга"

    slug = models.SlugField(unique=True, max_length=64)
    name_ky = models.CharField("Аталышы (кыргызча)", max_length=64)
    description_ky = models.CharField(
        "Сүрөттөмө (кыргызча)", max_length=160, blank=True, default=""
    )
    image = models.ImageField(upload_to="rewards/furniture/", blank=True, null=True)

    category = models.CharField(max_length=16, choices=RoomItemCategory.choices)
    price = models.PositiveIntegerField(help_text="Баасы тыйын менен")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бөлмө буюму"
        verbose_name_plural = "Бөлмө буюмдары"
        ordering = ["category", "price"]

    def __str__(self):
        return self.name_ky


class Room(models.Model):
    """
    Виртуальная комната ребёнка (одна на профиль в MVP). Хранит выбор
    фона — сам ассортимент мебели живёт в UserFurniture.
    """

    class Background(models.TextChoices):
        UY = "uy", "Заманбап үй бөлмөсү"
        BOZ_UI = "boz_ui", "Боз үй"

    profile = models.OneToOneField(
        "accounts.Profile", on_delete=models.CASCADE, related_name="room"
    )
    background = models.CharField(
        max_length=16, choices=Background.choices, default=Background.UY
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Бөлмө"
        verbose_name_plural = "Бөлмөлөр"

    def __str__(self):
        return f"Бөлмө: {self.profile}"


class UserFurniture(models.Model):
    """Конкретный предмет мебели, который ребёнок купил (и поставил в комнату)."""

    profile = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="owned_furniture"
    )
    furniture = models.ForeignKey(
        Furniture, on_delete=models.CASCADE, related_name="owned_by"
    )
    is_placed = models.BooleanField(
        default=True, help_text="Учурда бөлмөдө көрсөтүлүп жатабы"
    )
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сатылып алынган буюм"
        verbose_name_plural = "Сатылып алынган буюмдар"
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "furniture"], name="unique_profile_furniture"
            )
        ]

    def __str__(self):
        return f"{self.profile} — {self.furniture}"
