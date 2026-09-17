from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rewards.services import InsufficientFundsError

from .models import Furniture, Room
from .serializers import (
    FurnitureSerializer,
    PurchaseResultSerializer,
    RoomBackgroundUpdateSerializer,
    RoomSerializer,
)
from .services import AlreadyOwnedError, purchase_furniture


def _owned_furniture_ids(profile):
    return set(profile.owned_furniture.values_list("furniture_id", flat=True))


class FurnitureListView(ListAPIView):
    """GET /api/furniture/?category=carpet — каталог мебели для покупки."""

    serializer_class = FurnitureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Furniture.objects.filter(is_active=True)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["owned_furniture_ids"] = _owned_furniture_ids(self.request.user.profile)
        return context


class FurniturePurchaseView(APIView):
    """
    POST /api/furniture/{id}/purchase/
    Цена и списание тыйын полностью считаются на backend — см.
    apps.rooms.services.purchase_furniture и apps.rewards.services.spend_coins.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        furniture = get_object_or_404(Furniture, pk=pk, is_active=True)
        profile = request.user.profile

        try:
            purchase_furniture(profile, furniture)
        except AlreadyOwnedError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except InsufficientFundsError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_402_PAYMENT_REQUIRED)

        result = PurchaseResultSerializer(
            {
                "coins_spent": furniture.price,
                "new_balance": profile.coins_balance,
                "furniture": furniture,
            },
            context={"owned_furniture_ids": {furniture.id}},
        )
        return Response(result.data)


class MyRoomView(APIView):
    """
    GET  /api/rooms/me/  — текущий фон комнаты + расставленная мебель
    PATCH /api/rooms/me/ — сменить фон (background: "uy" | "boz_ui")
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        room, _ = Room.objects.get_or_create(profile=request.user.profile)
        return Response(RoomSerializer(room).data)

    def patch(self, request):
        room, _ = Room.objects.get_or_create(profile=request.user.profile)
        serializer = RoomBackgroundUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room.background = serializer.validated_data["background"]
        room.save(update_fields=["background", "updated_at"])
        return Response(RoomSerializer(room).data)
