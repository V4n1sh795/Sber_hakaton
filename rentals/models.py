from django.db import models
from users.models import User
from books.models import Book


class Rental(models.Model):
    """
    Аренда
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(null=False, blank=False)
    return_date = models.DateField(null=True, blank=True)
