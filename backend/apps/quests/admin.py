from django.contrib import admin

from .models import Quest, QuestAttempt, QuestOption


class QuestOptionInline(admin.TabularInline):
    model = QuestOption
    extra = 3


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("prompt_ky", "location", "quest_type", "correct_item", "reward_coins", "is_active")
    list_filter = ("location", "quest_type", "is_active")
    inlines = [QuestOptionInline]


@admin.register(QuestAttempt)
class QuestAttemptAdmin(admin.ModelAdmin):
    list_display = ("profile", "quest", "selected_item", "is_correct", "reward_granted", "created_at")
    list_filter = ("is_correct", "reward_granted")
    readonly_fields = [f.name for f in QuestAttempt._meta.fields]

    def has_add_permission(self, request):
        return False
