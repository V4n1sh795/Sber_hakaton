from django.db import models
from django.conf import settings
from books.models import BookCopy


class Rental(models.Model):
    """
    Аренда
    """
    book = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrow_date = models.DateField(null=False, blank=False)
    expected_return_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
