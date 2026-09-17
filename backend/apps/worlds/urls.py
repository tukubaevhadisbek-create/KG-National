from django.urls import path

from .views import CategoryListView, LocationListView

urlpatterns = [
    path("locations/", LocationListView.as_view(), name="location-list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
]
