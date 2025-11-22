from django.db import models
from django.conf import settings
from books.models import Book


class Favorite(models.Model):
    """
    Избранные книги
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_favorite_user_book'
            )
        ]
