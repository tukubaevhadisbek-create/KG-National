from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.achievements.services import check_and_unlock_achievements
from apps.progress.leveling import recalculate_level
from apps.progress.services import register_quest_completion, register_quest_result
from apps.rewards.models import RewardTransaction
from apps.rewards.services import grant_reward

from .models import Quest, QuestAttempt
from .serializers import (
    QuestAnswerRequestSerializer,
    QuestAnswerResultSerializer,
    QuestSerializer,
)

FEEDBACK_CORRECT = "Азамат! Туура таптың!"
FEEDBACK_INCORRECT = "Кайра аракет кылып көр."


class QuestListView(ListAPIView):
    """GET /api/quests/?location=uy"""

    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Quest.objects.filter(is_active=True).prefetch_related("options__item")
        location_slug = self.request.query_params.get("location")
        if location_slug:
            qs = qs.filter(location__slug=location_slug)
        return qs


class QuestAnswerView(APIView):
    """
    POST /api/quests/{id}/answer/
    body: {"selected_item_id": 12}

    Правильность проверяется ИСКЛЮЧИТЕЛЬНО на backend (сравнение с
    quest.correct_item_id). Награда начисляется только за первый
    правильный ответ на конкретный квест — повторные попытки не
    дают повторную оплату.
    """

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        quest = get_object_or_404(Quest, pk=pk, is_active=True)
        profile = request.user.profile

        request_serializer = QuestAnswerRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        selected_item_id = request_serializer.validated_data["selected_item_id"]

        is_correct = selected_item_id == quest.correct_item_id

        already_rewarded = QuestAttempt.objects.filter(
            profile=profile, quest=quest, reward_granted=True
        ).exists()

        QuestAttempt.objects.create(
            profile=profile,
            quest=quest,
            selected_item_id=selected_item_id,
            is_correct=is_correct,
            reward_granted=is_correct and not already_rewarded,
        )

        register_quest_result(profile, is_correct)

        coins_awarded = 0
        if is_correct and not already_rewarded:
            grant_reward(
                profile=profile,
                amount=quest.reward_coins,
                reason=RewardTransaction.Reason.QUEST_COMPLETED,
                source_type="quest",
                source_id=quest.id,
            )
            coins_awarded = quest.reward_coins
            register_quest_completion(profile)

        recalculate_level(profile)

        newly_unlocked = check_and_unlock_achievements(profile)

        result = QuestAnswerResultSerializer(
            {
                "is_correct": is_correct,
                "coins_awarded": coins_awarded,
                "new_balance": profile.coins_balance,
                "feedback_ky": FEEDBACK_CORRECT if is_correct else FEEDBACK_INCORRECT,
                "unlocked_achievements": newly_unlocked,
            }
        )
        return Response(result.data)
