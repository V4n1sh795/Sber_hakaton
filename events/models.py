from django.db import models

class Event(models.Model):
    """
    События
    """
    name = models.TextField(max_length=255, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(null=False, blank=False, max_digits=3, decimal_places=2, default=0.0)
