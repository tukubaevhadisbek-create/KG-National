from django.urls import path

from .views import QuestAnswerView, QuestListView

urlpatterns = [
    path("quests/", QuestListView.as_view(), name="quest-list"),
    path("quests/<int:pk>/answer/", QuestAnswerView.as_view(), name="quest-answer"),
]
