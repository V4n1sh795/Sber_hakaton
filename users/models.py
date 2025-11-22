from django.db import models

class UserRoles:
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
        ('Staff', 'Staff')
    ]


class User(models.Model):
    """
    Пользователь
    """
    name = models.TextField(null=False, blank=False)
    lastname = models.TextField(null=False, blank=False)
    patronymic = models.TextField(null=True, blank=True) # опционально
    role = models.TextField(null=False, blank=False, choices=UserRoles.ROLE_CHOICES)
    email = models.EmailField(null=True, blank=True) # опционально
    phone = models.TextField(null=True, blank=True, max_length=20) # опционально