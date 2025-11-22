from django.db import models

class CustomUser(AbstractUser):
    user_type = models.CharField(
        max_length=20,
        choices=[('reader', 'Reader'), ('staff', 'Staff')],
        default='reader'
    )

class Reader(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='reader_profile')
    reader_id = models.CharField(unique=True)
    
class Library(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    can_manage_readers = models.BooleanField(default=False)
    can_manage_books = models.BooleanField(default=False)
    can_manage_events = models.BooleanField(default=False)
