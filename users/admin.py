from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AirShopUser

@admin.register(AirShopUser)
class AirShopUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = UserAdmin.list_display + ('role',)
    list_filter = UserAdmin.list_filter + ('role',)
