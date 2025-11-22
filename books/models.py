from django.db import models


class Book(models.Model):
    """
    Книга
    """
    title = models.TextField(null=False, blank=False)
    author = models.TextField(null=False, blank=False)
    genre = models.TextField(null=False, blank=False)
    rating = models.DecimalField(null=False, blank=False, default=0.0)


class Photo(models.Model):
    """
    Фотографии (для ивентов, для экземпляров книг, ...)
    """
    image_data = models.BinaryField(null=False, blank=False)
    content_type = models.TextField(null=False, blank=False)
    uploaded_at = models.DateField(auto_now_add=True)

