from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Category, Location
from .serializers import CategorySerializer, LocationSerializer


class LocationListView(ListAPIView):
    """GET /api/locations/ — все активные локации с флагом is_locked."""

    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user_level"] = self.request.user.profile.level
        return context


class CategoryListView(ListAPIView):
    """GET /api/categories/"""

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
