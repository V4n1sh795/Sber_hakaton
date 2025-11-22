from django.contrib import admin
from django.utils.html import format_html
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'rating', 'photo_preview', 'created_at')
    list_filter = ('start_date', 'rating', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-start_date', '-created_at')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at', 'photo_preview')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'start_date', 'end_date', 'description')
        }),
        ('Медиа', {
            'fields': ('event_photo', 'photo_preview')
        }),
        ('Дополнительно', {
            'fields': ('rating',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def photo_preview(self, obj):
        """Превью фото в админке"""
        if obj.event_photo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.event_photo.url
            )
        return "Нет фото"
    photo_preview.short_description = 'Превью фото'
