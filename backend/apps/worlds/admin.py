from django.contrib import admin

from .models import Category, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name_ky", "slug", "order", "unlock_level", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name_ky",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_ky", "slug", "order")
    prepopulated_fields = {"slug": ("name_ky",)}
