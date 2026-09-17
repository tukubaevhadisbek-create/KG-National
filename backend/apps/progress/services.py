from django.db import transaction

from apps.accounts.models import Profile
from apps.items.models import Item

from .models import DiscoveredItem, UserProgress


@transaction.atomic
def register_item_discovery(profile: Profile, item: Item) -> tuple[bool, DiscoveredItem]:
    """
    Пытается зарегистрировать открытие предмета.
    Возвращает (created, discovered_item):
      created=True  — предмет открыт первый раз (нужно начислить награду)
      created=False — предмет уже был открыт раньше (награда не начисляется)
    """
    discovered_item, created = DiscoveredItem.objects.get_or_create(
        profile=profile, item=item
    )

    if created:
        progress, _ = UserProgress.objects.select_for_update().get_or_create(
            profile=profile
        )
        progress.items_found_count = progress.items_found_count + 1
        progress.words_learned_count = progress.words_learned_count + 1
        progress.save(update_fields=[
            "items_found_count", "words_learned_count", "updated_at"
        ])

    return created, discovered_item


@transaction.atomic
def register_quest_result(profile: Profile, is_correct: bool) -> UserProgress:
    """Обновляет счётчики после ответа на задание (quest)."""
    progress, _ = UserProgress.objects.select_for_update().get_or_create(
        profile=profile
    )
    if is_correct:
        progress.correct_answers_count = progress.correct_answers_count + 1
        progress.save(update_fields=["correct_answers_count", "updated_at"])
    return progress


@transaction.atomic
def register_quest_completion(profile: Profile) -> UserProgress:
    """Вызывается когда квест полностью завершён (не за каждый ответ)."""
    progress, _ = UserProgress.objects.select_for_update().get_or_create(
        profile=profile
    )
    progress.quests_completed_count = progress.quests_completed_count + 1
    progress.save(update_fields=["quests_completed_count", "updated_at"])
    return progress
