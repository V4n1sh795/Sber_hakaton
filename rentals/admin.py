from django.contrib import admin
from rentals.models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_title', 'user_name', 'status', 'created_at', 'borrow_date', 'is_expired', 'reservation_duration_hours']
    list_filter = ['status', 'created_at', 'borrow_date']
    search_fields = ['user__email', 'user__name', 'user__lastname', 'book__book__title']
    readonly_fields = ['created_at', 'confirmed_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('book', 'user', 'status')
        }),
        ('Даты', {
            'fields': ('created_at', 'confirmed_at', 'borrow_date', 'expected_return_date', 'return_date')
        }),
        ('Настройки брони', {
            'fields': ('reservation_duration_hours',),
            'description': 'Срок действия брони в часах (по умолчанию 48 часов = 2 суток)'
        }),
    )
    
    def book_title(self, obj):
        return obj.book.book.title
    book_title.short_description = 'Книга'
    
    def user_name(self, obj):
        return obj.user.full_name
    user_name.short_description = 'Пользователь'
    
    def is_expired(self, obj):
        return '✓ Истекла' if obj.is_expired else '—'
    is_expired.short_description = 'Истек срок'
    
    actions = ['confirm_rentals', 'cancel_rentals', 'issue_rentals']
    
    def confirm_rentals(self, request, queryset):
        updated = 0
        for rental in queryset.filter(status='pending'):
            rental.confirm()
            updated += 1
        self.message_user(request, f'Подтверждено бронирований: {updated}')
    confirm_rentals.short_description = 'Подтвердить выбранные брони'
    
    def cancel_rentals(self, request, queryset):
        updated = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(request, f'Отменено бронирований: {updated}')
    cancel_rentals.short_description = 'Отменить выбранные брони'
    
    def issue_rentals(self, request, queryset):
        updated = 0
        for rental in queryset.exclude(status__in=['cancelled', 'issued']):
            rental.issue()
            updated += 1
        self.message_user(request, f'Выдано книг: {updated}')
    issue_rentals.short_description = 'Выдать книги по выбранным броням'

