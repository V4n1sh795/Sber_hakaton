from django.db import models
from django.conf import settings
from books.models import Book


class Rental(models.Model):
    """
    Аренда
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrow_date = models.DateField(null=False, blank=False)
    return_date = models.DateField(null=True, blank=True)
