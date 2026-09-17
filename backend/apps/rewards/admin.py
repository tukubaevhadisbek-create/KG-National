from django.contrib import admin

from .models import RewardTransaction


@admin.register(RewardTransaction)
class RewardTransactionAdmin(admin.ModelAdmin):
    list_display = ("profile", "amount", "reason", "source_type", "source_id", "created_at")
    list_filter = ("reason",)
    search_fields = ("profile__first_name", "profile__telegram_id")
    readonly_fields = [f.name for f in RewardTransaction._meta.fields]

    def has_add_permission(self, request):
        # Транзакции создаются только сервисным слоем, руками — нельзя.
        return False

    def has_change_permission(self, request, obj=None):
        return False
