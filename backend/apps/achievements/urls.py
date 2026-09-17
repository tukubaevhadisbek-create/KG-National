from django.urls import path

from .views import AchievementListView

urlpatterns = [
    path("achievements/", AchievementListView.as_view(), name="achievement-list"),
]
