from django.db import models

class Event(models.Model):
    """
    События
    """
    name = models.TextField(max_length=255, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(null=False, blank=False, max_digits=3, decimal_places=2, default=0.0)
    event_photo = models.ImageField(
                            upload_to='events/photos/full/',
                            null=True, 
                            blank=True,
                            verbose_name='Обложка книги',
                            help_text='Загрузите фотографию книги'
                        )
    event_thumbnail = models.ImageField(
                            upload_to='events/photos/thumbnails/',
                            null=True, 
                            blank=True,
                            verbose_name='Превью обложки',
                            help_text='Генерируемая превью книги'
    )
