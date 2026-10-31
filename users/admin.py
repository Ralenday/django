from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'telefono', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('telefono',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('email', 'telefono')}),
    )
    ordering = ('id',)
