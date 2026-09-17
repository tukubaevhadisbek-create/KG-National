from rest_framework import serializers

from apps.achievements.serializers import UnlockedAchievementSerializer
from apps.items.models import Item

from .models import Quest, QuestOption


class QuestOptionSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source="item.id")
    item_name_ky = serializers.CharField(source="item.name_ky")
    item_image = serializers.ImageField(source="item.image")

    class Meta:
        model = QuestOption
        fields = ["item_id", "item_name_ky", "item_image"]


class QuestSerializer(serializers.ModelSerializer):
    """
    Отдаём фронту варианты, но НЕ указываем, какой из них правильный —
    проверка ответа целиком происходит на backend в /answer/.
    """

    options = QuestOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Quest
        fields = ["id", "quest_type", "prompt_ky", "reward_coins", "options"]


class QuestAnswerRequestSerializer(serializers.Serializer):
    selected_item_id = serializers.IntegerField()

    def validate_selected_item_id(self, value):
        if not Item.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Мындай буюм табылган жок")
        return value


class QuestAnswerResultSerializer(serializers.Serializer):
    is_correct = serializers.BooleanField()
    coins_awarded = serializers.IntegerField()
    new_balance = serializers.IntegerField()
    feedback_ky = serializers.CharField()
    unlocked_achievements = UnlockedAchievementSerializer(many=True)
