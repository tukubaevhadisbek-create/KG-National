from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.achievements.serializers import UnlockedAchievementSerializer
from apps.achievements.services import check_and_unlock_achievements
from apps.progress.leveling import recalculate_level
from apps.progress.services import register_item_discovery
from apps.rewards.models import RewardTransaction
from apps.rewards.services import grant_reward

from .models import Item
from .serializers import DiscoverResultSerializer, ItemDetailSerializer, ItemListSerializer


def _discovered_ids_for(profile):
    return set(
        profile.discovered_items.values_list("item_id", flat=True)
    )


class ItemListView(ListAPIView):
    """
    GET /api/items/?location=uy&category=uy-buyumdaru
    Список активных предметов, с фильтрами по локации/категории (по slug).
    """

    serializer_class = ItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Item.objects.filter(is_active=True).select_related("location", "category")
        location_slug = self.request.query_params.get("location")
        category_slug = self.request.query_params.get("category")
        if location_slug:
            qs = qs.filter(location__slug=location_slug)
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["discovered_item_ids"] = _discovered_ids_for(self.request.user.profile)
        return context


class ItemDetailView(RetrieveAPIView):
    """GET /api/items/{id}/"""

    serializer_class = ItemDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["discovered_item_ids"] = _discovered_ids_for(self.request.user.profile)
        return context


class ItemDiscoverView(APIView):
    """
    POST /api/items/{id}/discover/
    Ребёнок нажал на предмет. Если это первое открытие — начисляем
    discover_reward тыйын и обновляем прогресс. Вся логика награды
    считается на backend, frontend только сообщает "какой предмет".
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk, is_active=True)
        profile = request.user.profile

        created, _discovered = register_item_discovery(profile, item)

        coins_awarded = 0
        if created:
            grant_reward(
                profile=profile,
                amount=item.discover_reward,
                reason=RewardTransaction.Reason.ITEM_DISCOVERED,
                source_type="item",
                source_id=item.id,
            )
            coins_awarded = item.discover_reward

        # Уровень пересчитывается на сервере из числа найденных
        # предметов — от него зависит открытие новых локаций.
        recalculate_level(profile)

        newly_unlocked = check_and_unlock_achievements(profile)

        result = DiscoverResultSerializer(
            {
                "already_discovered": not created,
                "coins_awarded": coins_awarded,
                "new_balance": profile.coins_balance,
                # Передаём саму модель, а не уже сериализованные данные —
                # вложенный ItemDetailSerializer сам превратит её в JSON.
                "item": item,
                "unlocked_achievements": newly_unlocked,
            },
            context={"discovered_item_ids": {item.id}},
        )
        return Response(result.data)
