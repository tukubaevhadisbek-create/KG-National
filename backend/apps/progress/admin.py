from django.contrib import admin

from .models import DiscoveredItem, UserProgress


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = (
        "profile", "words_learned_count", "items_found_count",
        "quests_completed_count", "correct_answers_count",
    )
    search_fields = ("profile__first_name",)


@admin.register(DiscoveredItem)
class DiscoveredItemAdmin(admin.ModelAdmin):
    list_display = ("profile", "item", "discovered_at")
    search_fields = ("profile__first_name", "item__name_ky")
