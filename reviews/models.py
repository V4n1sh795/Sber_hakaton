from django.db import models
from users.models import User
from books.models import Book
from events.models import Event
from rentals.models import Rental

class RatingConstants:
    RATING_CHOICES = [
        (1, 'Ужасно'),
        (2, 'Плохо'),
        (3, 'Неплохо'),
        (4, 'Хорошо'),
        (5, 'Отлично')
    ]

class Review(models.Model):
    """
    База для отзыва (абстрактная, для этого таблица не будет создана)
    """
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class ReviewBook(Review):
    """
    Отзыв на книгу
    """
    book = models.ForeignKey(Book, null=False, blank=False, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False, blank=False, choices=RatingConstants.RATING_CHOICES)

class ReviewRental(Review):
    """
    Отзыв на конкретное бронирование
    """
    rental = models.ForeignKey(Rental, null=False, blank=False, on_delete=models.CASCADE)

class ReviewEvent(Review):
    """
    Отзыв на событие
    """
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False, blank=False, choices=RatingConstants.RATING_CHOICES)