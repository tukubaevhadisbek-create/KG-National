from django.db import models


class Location(models.Model):
    """
    Локация виртуального мира: Үй, Айыл, Жайлоо, Боз үй, Ат сарай.
    slug используется во frontend-роутинге (например /world/uy).
    """

    slug = models.SlugField(unique=True, max_length=32)
    name_ky = models.CharField("Аталышы (кыргызча)", max_length=64)
    description_ky = models.TextField("Сүрөттөмө (кыргызча)", blank=True, default="")
    background_image = models.ImageField(
        upload_to="locations/backgrounds/", blank=True, null=True
    )
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    # Начиная с какого уровня профиля локация открыта. MVP: только Үй (0).
    unlock_level = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локациялар"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_ky


class Category(models.Model):
    """
    Категория предметов: Үй буюмдары, Улуттук буюмдар, Тамак-аш,
    Музыкалык аспаптар, Ат жабдыктары, Табият, Үй-бүлө и т.д.
    """

    slug = models.SlugField(unique=True, max_length=32)
    name_ky = models.CharField("Аталышы (кыргызча)", max_length=64)
    icon = models.ImageField(upload_to="ui/categories/", blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_ky
