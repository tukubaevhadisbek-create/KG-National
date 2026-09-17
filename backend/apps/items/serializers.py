from rest_framework import serializers

from apps.achievements.serializers import UnlockedAchievementSerializer

from .models import Item


class ItemListSerializer(serializers.ModelSerializer):
    """Короткая карточка для списков/локации — без полного текста факта."""

    is_discovered = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "slug",
            "name_ky",
            "image",
            "category",
            "location",
            "difficulty",
            "is_discovered",
        ]

    def get_is_discovered(self, obj):
        discovered_ids = self.context.get("discovered_item_ids", set())
        return obj.id in discovered_ids


class ItemDetailSerializer(serializers.ModelSerializer):
    """Полная карточка предмета — открывается по нажатию."""

    is_discovered = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "slug",
            "name_ky",
            "description_ky",
            "cultural_fact_ky",
            "image",
            "audio",
            "category",
            "location",
            "difficulty",
            "discover_reward",
            "is_discovered",
        ]

    def get_is_discovered(self, obj):
        discovered_ids = self.context.get("discovered_item_ids", set())
        return obj.id in discovered_ids


class DiscoverResultSerializer(serializers.Serializer):
    """Ответ POST /api/items/{id}/discover/"""

    already_discovered = serializers.BooleanField()
    coins_awarded = serializers.IntegerField()
    new_balance = serializers.IntegerField()
    item = ItemDetailSerializer()
    unlocked_achievements = UnlockedAchievementSerializer(many=True)
