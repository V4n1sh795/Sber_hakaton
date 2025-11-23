from django.db import models
from django.conf import settings
from django.utils import timezone
from books.models import BookCopy


class Rental(models.Model):
    """
    Аренда/Бронирование книги
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('issued', 'Выдано'),
        ('returned', 'Возвращено'),
        ('cancelled', 'Отменено'),
    ]
    
    book = models.ForeignKey(BookCopy, on_delete=models.CASCADE, verbose_name='Экземпляр книги')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания брони')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата подтверждения')
    borrow_date = models.DateField(null=False, blank=False, verbose_name='Дата выдачи')
    expected_return_date = models.DateField(null=True, blank=True, verbose_name='Ожидаемая дата возврата')
    return_date = models.DateField(null=True, blank=True, verbose_name='Фактическая дата возврата')
    
    # Срок действия брони (в часах)
    reservation_duration_hours = models.IntegerField(default=48, verbose_name='Срок действия брони (часов)')
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Бронь #{self.pk} - {self.book.book.title} ({self.get_status_display()})"
    
    @property
    def is_expired(self):
        """Проверяет, истек ли срок брони"""
        if self.status not in ['pending', 'confirmed']:
            return False
        
        from datetime import timedelta
        expiry_time = self.created_at + timedelta(hours=self.reservation_duration_hours)
        return timezone.now() > expiry_time
    
    @property
    def expiry_time(self):
        """Возвращает время истечения брони"""
        from datetime import timedelta
        return self.created_at + timedelta(hours=self.reservation_duration_hours)
    
    def confirm(self, confirmed_by=None):
        """Подтверждает бронирование"""
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.save()
    
    def cancel(self):
        """Отменяет бронирование"""
        self.status = 'cancelled'
        self.save()
    
    def issue(self):
        """Помечает как выданное"""
        self.status = 'issued'
        self.save()
    
    def return_book(self):
        """Помечает книгу как возвращенную"""
        self.status = 'returned'
        self.return_date = timezone.now().date()
        self.save()
