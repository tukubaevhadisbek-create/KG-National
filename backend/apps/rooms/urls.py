from django.urls import path

from .views import FurnitureListView, FurniturePurchaseView, MyRoomView

urlpatterns = [
    path("furniture/", FurnitureListView.as_view(), name="furniture-list"),
    path("furniture/<int:pk>/purchase/", FurniturePurchaseView.as_view(), name="furniture-purchase"),
    path("rooms/me/", MyRoomView.as_view(), name="my-room"),
]
