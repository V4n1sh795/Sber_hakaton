from django.contrib import admin
from django.utils.html import format_html
from .models import Event, EventSubscription


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'rating', 'subscribers_count', 'photo_preview', 'created_at')
    list_filter = ('start_date', 'rating', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-start_date', '-created_at')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at', 'photo_preview', 'subscribers_count')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'start_date', 'end_date', 'description')
        }),
        ('Медиа', {
            'fields': ('event_photo', 'photo_preview')
        }),
        ('Дополнительно', {
            'fields': ('rating', 'subscribers_count')
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
    
    def subscribers_count(self, obj):
        """Количество подписчиков"""
        count = obj.eventsubscription_set.filter(status='active').count()
        return format_html('<b>{}</b>', count)
    subscribers_count.short_description = 'Подписчиков'


@admin.register(EventSubscription)
class EventSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'reminder_type', 'status', 'reminder_24h_sent', 'reminder_1h_sent', 'subscribed_at')
    list_filter = ('status', 'reminder_type', 'reminder_24h_sent', 'reminder_1h_sent', 'subscribed_at')
    search_fields = ('event__name', 'user__email', 'user__name', 'user__lastname')
    ordering = ('-subscribed_at',)
    date_hierarchy = 'subscribed_at'
    readonly_fields = ('subscribed_at',)
    
    fieldsets = (
        ('Подписка', {
            'fields': ('event', 'user', 'status')
        }),
        ('Напоминания', {
            'fields': ('reminder_type', 'reminder_24h_sent', 'reminder_1h_sent')
        }),
        ('Дата подписки', {
            'fields': ('subscribed_at',)
        }),
    )
    
    list_select_related = ('event', 'user')
