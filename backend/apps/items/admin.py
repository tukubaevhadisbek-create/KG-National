from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name_ky", "slug", "location", "category", "difficulty",
        "discover_reward", "is_active",
    )
    list_filter = ("location", "category", "difficulty", "is_active")
    search_fields = ("name_ky", "slug", "description_ky")
    prepopulated_fields = {"slug": ("name_ky",)}
    fieldsets = (
        (None, {"fields": ("slug", "location", "category", "is_active")}),
        ("Мазмун (кыргызча)", {
            "fields": ("name_ky", "description_ky", "cultural_fact_ky")
        }),
        ("Медиа", {"fields": ("image", "audio")}),
        ("Оюн параметрлери", {"fields": ("difficulty", "discover_reward")}),
    )
