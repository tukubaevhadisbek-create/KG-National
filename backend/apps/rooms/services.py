from django.db import transaction

from apps.accounts.models import Profile
from apps.rewards.models import RewardTransaction
from apps.rewards.services import InsufficientFundsError, spend_coins  # noqa: F401 (реэкспорт для views)

from .models import Furniture, UserFurniture


class AlreadyOwnedError(Exception):
    """Ребёнок уже купил этот предмет мебели раньше."""


@transaction.atomic
def purchase_furniture(profile: Profile, furniture: Furniture) -> UserFurniture:
    """
    Покупка предмета мебели за тыйын. Цена берётся ИСКЛЮЧИТЕЛЬНО из
    Furniture.price на backend — frontend не может прислать свою цену.
    Бросает AlreadyOwnedError, если предмет уже куплен, и
    InsufficientFundsError (из apps.rewards.services), если тыйын не хватает.
    """
    if UserFurniture.objects.filter(profile=profile, furniture=furniture).exists():
        raise AlreadyOwnedError("Бул буюм мурда эле сатылып алынган")

    spend_coins(
        profile=profile,
        amount=furniture.price,
        reason=RewardTransaction.Reason.FURNITURE_PURCHASE,
        source_type="furniture",
        source_id=furniture.id,
    )

    return UserFurniture.objects.create(profile=profile, furniture=furniture)
