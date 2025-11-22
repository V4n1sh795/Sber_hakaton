from django.db import models


class Book(models.Model):
    """
    Книга
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    genre = models.CharField(max_length=255, null=False, blank=False)
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
