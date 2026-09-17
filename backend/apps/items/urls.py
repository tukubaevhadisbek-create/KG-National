from django.urls import path

from .views import ItemDetailView, ItemDiscoverView, ItemListView

urlpatterns = [
    path("items/", ItemListView.as_view(), name="item-list"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("items/<int:pk>/discover/", ItemDiscoverView.as_view(), name="item-discover"),
]
