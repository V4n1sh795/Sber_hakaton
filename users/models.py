from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRoles:
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
        ('Staff', 'Staff')
    ]


class CustomUser(AbstractUser):
    """
    Пользователь
    """
    name = models.TextField(null=False, blank=False)
    lastname = models.TextField(null=False, blank=False)
    patronymic = models.TextField(null=True, blank=True) # опционально
    role = models.TextField(null=False, blank=False, choices=UserRoles.ROLE_CHOICES)# опционально
    phone = models.TextField(null=True, blank=True, max_length=20) # опционально
    email = models.EmailField('email', unique=True)
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['name', 'lastname'] 