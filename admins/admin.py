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
        # 'groups', 'user_permissions' 추가
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'groups', 'user_permissions' 추가
            'fields': ('admin_id', 'email', 'cell_num', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    search_fields = ('email', 'admin_id')
    ordering = ('admins_id',)
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Admin, CustomUserAdmin)
