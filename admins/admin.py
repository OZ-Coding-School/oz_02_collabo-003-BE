# admins/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Admin

class CustomUserAdmin(UserAdmin):
    model = Admin
    list_display = ('email', 'admin_id', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('admin_id', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('admin_id', 'email', 'cell_num', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'admin_id')
    ordering = ('admins_id',)
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Admin, CustomUserAdmin)
