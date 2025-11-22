from django.db import models
from users.models import User
from books.models import Book

class Favorite(models.Model):
    """
    Избранные книги
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
