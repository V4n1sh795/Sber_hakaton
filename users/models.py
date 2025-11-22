from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Пользователь библиотечной системы.
    
    Типы пользователей:
    - Обычный пользователь (is_staff=False, is_superuser=False): читатели библиотеки
    - Сотрудник библиотеки (is_staff=True): единый аккаунт для всех библиотекарей
    - Суперадмин (is_superuser=True): администратор системы
    """
    name = models.CharField(max_length=150, verbose_name='Имя')
    lastname = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name='Отчество')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    email = models.EmailField('email', unique=True)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['name', 'lastname']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.lastname} {self.name} ({self.email})"
    
    @property
    def full_name(self):
        """Возвращает полное имя пользователя"""
        if self.patronymic:
            return f"{self.lastname} {self.name} {self.patronymic}"
        return f"{self.lastname} {self.name}"
    
    @property
    def role_display(self):
        """Возвращает роль пользователя для отображения"""
        if self.is_superuser:
            return 'Суперадмин'
        elif self.is_staff:
            return 'Сотрудник библиотеки'
        else:
            return 'Читатель' 