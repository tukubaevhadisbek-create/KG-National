"""
Единственное место в проекте, которое имеет право менять баланс
тыйын. Все остальные части кода (items, quests, rooms, ...) должны
вызывать grant_reward()/spend_coins() вместо прямой правки
Profile.coins_balance.
"""

from django.db import transaction

from apps.accounts.models import Profile

from .models import RewardTransaction


class InsufficientFundsError(Exception):
    """Попытка потратить больше тыйын, чем есть на балансе."""


@transaction.atomic
def grant_reward(
    profile: Profile,
    amount: int,
    reason: str,
    source_type: str = "",
    source_id: int | None = None,
) -> RewardTransaction:
    """
    Создаёт запись в журнале и атомарно обновляет кэш баланса.
    amount должен быть > 0 — для списаний используйте spend_coins().
    """
    if amount <= 0:
        raise ValueError("Сыйлык суммасы 0деи чоц болушу керек")

    locked_profile = Profile.objects.select_for_update().get(pk=profile.pk)

    reward_tx = RewardTransaction.objects.create(
        profile=locked_profile,
        amount=amount,
        reason=reason,
        source_type=source_type,
        source_id=source_id,
    )

    locked_profile.coins_balance = locked_profile.coins_balance + amount
    locked_profile.save(update_fields=["coins_balance", "updated_at"])

    profile.coins_balance = locked_profile.coins_balance
    return reward_tx


@transaction.atomic
def spend_coins(
    profile: Profile,
    amount: int,
    reason: str,
    source_type: str = "",
    source_id: int | None = None,
) -> RewardTransaction:
    """
    Списывает тыйын (например, при покупке мебели). Баланс проверяется
    под блокировкой строки (select_for_update), поэтому два
    одновременных запроса не смогут увести баланс в минус — это и есть
    "серверная проверка наград", о которой говорилось в ТЗ (раздел 21).
    """
    if amount <= 0:
        raise ValueError("Чыгаша суммасы 0деи чоц болушу керек")

    locked_profile = Profile.objects.select_for_update().get(pk=profile.pk)

    if locked_profile.coins_balance < amount:
        raise InsufficientFundsError("Тыйын жетишсиз")

    reward_tx = RewardTransaction.objects.create(
        profile=locked_profile,
        amount=-amount,
        reason=reason,
        source_type=source_type,
        source_id=source_id,
    )

    locked_profile.coins_balance = locked_profile.coins_balance - amount
    locked_profile.save(update_fields=["coins_balance", "updated_at"])

    profile.coins_balance = locked_profile.coins_balance
    return reward_tx
