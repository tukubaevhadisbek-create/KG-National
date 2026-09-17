"""
Проверка и открытие достижений. Вызывается после любого действия,
которое могло изменить счётчики UserProgress (открытие предмета,
завершение квеста) — см. apps.items.views.ItemDiscoverView и
apps.quests.views.QuestAnswerView.
"""

from django.db import transaction

from apps.accounts.models import Profile
from apps.progress.models import UserProgress

from .models import Achievement, UserAchievement

# Какое поле UserProgress соответствует каждому типу условия.
PROGRESS_FIELD_BY_CONDITION = {
    Achievement.ConditionType.ITEMS_FOUND: "items_found_count",
    Achievement.ConditionType.QUESTS_COMPLETED: "quests_completed_count",
    Achievement.ConditionType.WORDS_LEARNED: "words_learned_count",
    Achievement.ConditionType.CORRECT_ANSWERS: "correct_answers_count",
}


@transaction.atomic
def check_and_unlock_achievements(profile: Profile) -> list[UserAchievement]:
    """
    Проверяет все ещё не открытые достижения профиля и открывает те,
    условие которых уже выполнено. Возвращает список новых
    UserAchievement (обычно 0 или 1, но может быть несколько сразу,
    если один Item.discover() перепрыгнул сразу через два порога).
    """
    progress, _ = UserProgress.objects.get_or_create(profile=profile)

    already_unlocked_ids = set(
        UserAchievement.objects.filter(profile=profile).values_list(
            "achievement_id", flat=True
        )
    )

    candidates = Achievement.objects.filter(is_active=True).exclude(
        id__in=already_unlocked_ids
    )

    newly_unlocked = []
    for achievement in candidates:
        field_name = PROGRESS_FIELD_BY_CONDITION.get(achievement.condition_type)
        if field_name is None:
            continue

        current_value = getattr(progress, field_name)
        if current_value < achievement.threshold:
            continue

        user_achievement = UserAchievement.objects.create(
            profile=profile, achievement=achievement
        )
        newly_unlocked.append(user_achievement)

        if achievement.reward_coins > 0:
            from apps.rewards.models import RewardTransaction
            from apps.rewards.services import grant_reward

            grant_reward(
                profile=profile,
                amount=achievement.reward_coins,
                reason=RewardTransaction.Reason.BONUS,
                source_type="achievement",
                source_id=achievement.id,
            )

    return newly_unlocked
