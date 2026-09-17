# -*- coding: utf-8 -*-
"""
Уровень ребёнка (Profile.level).

Правило простое и полностью серверное: уровень = 1 + (число
найденных предметов // 10). Уровень нельзя «накрутить» с фронтенда —
он пересчитывается из UserProgress, который меняется только
сервисным слоем backend'а.

Уровень нужен для открытия новых локаций (Location.unlock_level).
"""

from django.db import transaction

from apps.accounts.models import Profile

from .models import UserProgress

ITEMS_PER_LEVEL = 10


def level_for(items_found: int) -> int:
    return 1 + items_found // ITEMS_PER_LEVEL


@transaction.atomic
def recalculate_level(profile: Profile) -> int:
    """Пересчитывает и при необходимости сохраняет уровень. Возвращает уровень."""
    progress, _ = UserProgress.objects.get_or_create(profile=profile)
    new_level = level_for(progress.items_found_count)

    if new_level != profile.level:
        locked = Profile.objects.select_for_update().get(pk=profile.pk)
        locked.level = new_level
        locked.save(update_fields=["level", "updated_at"])
        profile.level = new_level

    return new_level
