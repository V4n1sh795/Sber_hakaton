from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Настройка админ-панели для управления пользователями
    """
    list_display = ('email', 'full_name', 'role_display', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'name', 'lastname', 'phone')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('email', 'password')
        }),
        ('Персональные данные', {
            'fields': ('name', 'lastname', 'patronymic', 'phone')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'is_staff - сотрудник библиотеки, is_superuser - суперадмин'
        }),
        ('Даты', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Создание пользователя', {
            'classes': ('wide',),
            'fields': ('email', 'name', 'lastname', 'patronymic', 'phone', 
                      'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
