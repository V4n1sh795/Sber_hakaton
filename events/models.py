from django.db import models
from django.urls import reverse


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
