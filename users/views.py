
# myapp/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser


def autorization_page(request):
    """
    Страница выбора между входом и регистрацией (регистрация только для staff)
    """
    return render(request, 'users/auth.html')


def login_view(request):
    """
    Вход в систему для всех типов пользователей
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            # Перенаправляем в зависимости от роли
            if user.is_staff or user.is_superuser:
                return redirect('/admin/')  # Админ-панель для staff и superuser
            else:
                return redirect('/users/profile')  # Личный кабинет для обычных пользователей
        else:
            messages.error(request, "Неверный email или пароль.")
    
    return render(request, 'users/login.html')


@login_required
def profile_view(request):
    """
    Профиль пользователя
    """
    return render(request, 'users/profile.html', {'user': request.user})