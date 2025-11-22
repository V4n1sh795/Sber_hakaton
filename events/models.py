from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):
    """
    События библиотеки (лекции, встречи, выставки и т.д.)
    """
    name = models.CharField(max_length=255, verbose_name='Название события')
    start_date = models.DateTimeField(verbose_name='Дата и время начала')
    end_date = models.DateTimeField(verbose_name='Дата и время окончания')
    description = models.TextField(blank=True, verbose_name='Описание')
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.0,
        verbose_name='Рейтинг'
    )
    event_photo = models.ImageField(
        upload_to='events/photos/full/',
        null=True, 
        blank=True,
        verbose_name='Фото события',
        help_text='Загрузите фотографию события'
    )
    event_thumbnail = models.ImageField(
        upload_to='events/photos/thumbnails/',
        null=True, 
        blank=True,
        verbose_name='Превью фото',
        help_text='Автоматически генерируемое превью'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['-start_date', '-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.start_date.strftime('%d.%m.%Y %H:%M')})"
    
    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})
    
    def is_upcoming(self):
        """Проверка, что событие ещё не началось"""
        return self.start_date > timezone.now()


class EventSubscription(models.Model):
    """Подписка пользователя на событие"""
    
    REMINDER_CHOICES = [
        ('24h', '24 часа до события'),
        ('2h', '2 часа до события'),
        ('both', '24 часа и 2 часа'),
        ('none', 'Без напоминаний'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('unsubscribed', 'Отписан'),
        ('expired', 'Истекла'),
    ]
    
    # Связи
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='event_subscriptions',
        verbose_name='Подписчик'
    )
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Событие'
    )
    
    # Параметры подписки
    reminder_type = models.CharField(
        max_length=10,
        choices=REMINDER_CHOICES,
        default='both',
        verbose_name='Тип напоминания'
    )
    
    # Статус
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
    )
    
    # Отслеживание отправки напоминаний
    reminder_24h_sent = models.BooleanField(
        default=False,
        verbose_name='Напоминание за 24ч отправлено'
    )
    reminder_1h_sent = models.BooleanField(
        default=False,
        verbose_name='Напоминание за 2ч отправлено'
    )
    
    # Даты
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Подписка на событие'
        verbose_name_plural = 'Подписки на события'
        unique_together = [['user', 'event']]
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return f"{self.user} подписан на {self.event}"
    
    def reset_reminders(self):
        """Сбросить флаги напоминаний (для пересчета)"""
        self.reminder_24h_sent = False
        self.reminder_1h_sent = False
        self.save()
    
    def is_valid_subscription(self):
        """Активна ли подписка"""
        return self.status == 'active' and self.event.is_upcoming()

