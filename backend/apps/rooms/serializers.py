from rest_framework import serializers

from .models import Furniture, Room, UserFurniture


class FurnitureSerializer(serializers.ModelSerializer):
    """Для каталога /api/furniture/ — с флагом, куплен ли уже предмет."""

    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = Furniture
        fields = [
            "id", "slug", "name_ky", "description_ky", "image",
            "category", "price", "is_owned",
        ]

    def get_is_owned(self, obj):
        owned_ids = self.context.get("owned_furniture_ids", set())
        return obj.id in owned_ids


class OwnedFurnitureSerializer(serializers.ModelSerializer):
    """Мебель, стоящая в комнате ребёнка — для /api/rooms/me/."""

    id = serializers.IntegerField(source="furniture.id")
    slug = serializers.SlugField(source="furniture.slug")
    name_ky = serializers.CharField(source="furniture.name_ky")
    image = serializers.ImageField(source="furniture.image")
    category = serializers.CharField(source="furniture.category")

    class Meta:
        model = UserFurniture
        fields = ["id", "slug", "name_ky", "image", "category", "is_placed"]


class RoomSerializer(serializers.ModelSerializer):
    placed_furniture = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["background", "placed_furniture"]

    def get_placed_furniture(self, obj):
        items = obj.profile.owned_furniture.filter(is_placed=True).select_related("furniture")
        return OwnedFurnitureSerializer(items, many=True).data


class RoomBackgroundUpdateSerializer(serializers.Serializer):
    background = serializers.ChoiceField(choices=Room.Background.choices)


class PurchaseResultSerializer(serializers.Serializer):
    coins_spent = serializers.IntegerField()
    new_balance = serializers.IntegerField()
    furniture = FurnitureSerializer()
