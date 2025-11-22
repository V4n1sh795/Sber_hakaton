from django.db import models
from users.models import User
from books.models import Book

class Favorite(models.Model):
    """
    Избранные книги
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_favorite_user_book'
            )
        ]
