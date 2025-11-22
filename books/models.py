from django.db import models


class Book(models.Model):
    """
    Книга
    """
    title = models.TextField(null=False, blank=False)
    author = models.TextField(null=False, blank=False)
    genre = models.TextField(null=False, blank=False)
    rating = models.DecimalField(null=False, blank=False, max_digits=3, decimal_places=2, default=0.0)
    cover_photo = models.ImageField(
                            upload_to='covers/full/',
                            null=True, 
                            blank=True,
                            verbose_name='Обложка книги',
                            help_text='Загрузите фотографию книги'
                        )
    cover_thumbnail = models.ImageField(
                            upload_to='covers/thumbnails/',
                            null=True, 
                            blank=True,
                            verbose_name='Превью обложки',
                            help_text='Генерируемая превью книги'
    )
