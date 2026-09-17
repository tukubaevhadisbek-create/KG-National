from rest_framework import serializers

from .models import UserProgress


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = [
            "words_learned_count",
            "items_found_count",
            "quests_completed_count",
            "correct_answers_count",
            "updated_at",
        ]
