from django.db import models
from django.conf import settings
from books.models import Book
from events.models import Event


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)
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

class ReviewServiceQuality(Review):
    """
    Отзыв о качестве обслуживания
    """
    rating = models.IntegerField(null=False, blank=False, choices=RatingConstants.RATING_CHOICES)

class ReviewEvent(Review):
    """
    Отзыв на событие
    """
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False, blank=False, choices=RatingConstants.RATING_CHOICES)