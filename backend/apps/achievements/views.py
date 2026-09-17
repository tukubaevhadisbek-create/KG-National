from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Achievement, UserAchievement
from .serializers import AchievementSerializer


class AchievementListView(ListAPIView):
    """
    GET /api/achievements/
    Список всех достижений с флагом is_unlocked для текущего ребёнка —
    именно на этом строится экран "Менин жетишкендиктерим".
    """

    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    queryset = Achievement.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        unlocked = UserAchievement.objects.filter(profile=self.request.user.profile)
        context["unlocked_map"] = {ua.achievement_id: ua for ua in unlocked}
        return context
