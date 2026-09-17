from django.contrib import admin

from .models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title_ky", "slug", "condition_type", "threshold", "reward_coins", "is_active")
    list_filter = ("condition_type", "is_active")
    prepopulated_fields = {"slug": ("title_ky",)}


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ("profile", "achievement", "unlocked_at")
    readonly_fields = [f.name for f in UserAchievement._meta.fields]

    def has_add_permission(self, request):
        # Открывается только автоматически через check_and_unlock_achievements.
        return False
