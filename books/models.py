from django.db import models


class Book(models.Model):
    """
    Книга
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    genre = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
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

class BookCopy(models.Model):
    """
    Экземпляр книги
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_condition_photo = models.ImageField(
                            upload_to='copies/condition/full/',
                            null=True, 
                            blank=True,
                            verbose_name='Фотография состояния книги',
                            help_text='Загрузите фотографию исходного состояния книги'
                        )
    registered_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)