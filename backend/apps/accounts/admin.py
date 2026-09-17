from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "telegram_id", "level", "coins_balance", "created_at")
    search_fields = ("first_name", "telegram_username", "telegram_id")
    readonly_fields = ("coins_balance", "created_at", "updated_at")
