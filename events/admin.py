from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'rating')
    list_filter = ('date', 'rating')
    search_fields = ('name', 'description')
    ordering = ('-date',)
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'date')
        }),
        ('Дополнительно', {
            'fields': ('description', 'rating')
        }),
    )
