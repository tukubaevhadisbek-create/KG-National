from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import UserProgress
from .serializers import UserProgressSerializer


class MyProgressView(RetrieveAPIView):
    """GET /api/progress/me/"""

    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        progress, _ = UserProgress.objects.get_or_create(
            profile=self.request.user.profile
        )
        return progress
