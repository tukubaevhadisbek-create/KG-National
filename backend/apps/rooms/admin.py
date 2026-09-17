from django.contrib import admin

from .models import Furniture, Room, UserFurniture


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ("name_ky", "slug", "category", "price", "is_active")
    list_filter = ("category", "is_active")
    prepopulated_fields = {"slug": ("name_ky",)}


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("profile", "background", "updated_at")


@admin.register(UserFurniture)
class UserFurnitureAdmin(admin.ModelAdmin):
    list_display = ("profile", "furniture", "is_placed", "purchased_at")
    list_filter = ("is_placed",)

    def has_add_permission(self, request):
        # Мебель попадает сюда только через покупку (services.purchase_furniture).
        return False
