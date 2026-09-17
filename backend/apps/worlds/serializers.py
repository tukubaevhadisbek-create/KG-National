from rest_framework import serializers

from .models import Category, Location


class LocationSerializer(serializers.ModelSerializer):
    # Поле, которое покажет frontend'у, доступна ли локация ребёнку
    # при его текущем уровне (level передаётся из UserProgress/Profile).
    is_locked = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            "id",
            "slug",
            "name_ky",
            "description_ky",
            "background_image",
            "unlock_level",
            "is_locked",
        ]

    def get_is_locked(self, obj):
        user_level = self.context.get("user_level", 1)
        return user_level < obj.unlock_level


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "name_ky", "icon"]
