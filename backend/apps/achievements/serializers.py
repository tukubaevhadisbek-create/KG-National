from rest_framework import serializers

from .models import Achievement, UserAchievement


class AchievementSerializer(serializers.ModelSerializer):
    """Для списка /api/achievements/ — с флагом, открыто ли уже ребёнком."""

    is_unlocked = serializers.SerializerMethodField()
    unlocked_at = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = [
            "id", "slug", "title_ky", "description_ky", "icon",
            "threshold", "condition_type", "is_unlocked", "unlocked_at",
        ]

    def get_is_unlocked(self, obj):
        unlocked_map = self.context.get("unlocked_map", {})
        return obj.id in unlocked_map

    def get_unlocked_at(self, obj):
        unlocked_map = self.context.get("unlocked_map", {})
        ua = unlocked_map.get(obj.id)
        return ua.unlocked_at if ua else None


class UnlockedAchievementSerializer(serializers.ModelSerializer):
    """
    Компактная версия — используется для мгновенного уведомления
    ребёнка сразу после действия (см. items/quests views), когда
    достижение открылось прямо сейчас. instance здесь — UserAchievement.
    """

    title_ky = serializers.CharField(source="achievement.title_ky")
    description_ky = serializers.CharField(source="achievement.description_ky")
    icon = serializers.ImageField(source="achievement.icon")
    reward_coins = serializers.IntegerField(source="achievement.reward_coins")

    class Meta:
        model = UserAchievement
        fields = ["title_ky", "description_ky", "icon", "reward_coins"]
