
# myapp/views.py
# myapp/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, UserRoles
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def autorization_page(request):
    return render(request, 'users/auth.html')

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        lastname = request.POST.get('lastname')
        patronymic = request.POST.get('patronymic')
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        print('ass')
        print(email, password, name, lastname, patronymic, role, phone)
        if not (email and password and name and lastname and role):
            messages.error(request, "Заполните обязательные поля.")
            return render(request, 'users/auth.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует.")
            return render(request, 'users/profile.html')
        
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            name=name,
            lastname=lastname,
            patronymic=patronymic,
            role=role,
            phone=phone
        )

        user.save()
        messages.success(request, "Пользователь успешно зарегистрирован.")
        return redirect('/users/login')  # или сразу в профиль, если хотите
    else:
        return render(request, 'users/auth.html')

    return JsonResponse({'error': 'Только POST'}, status=405)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/users/profile')  # указать имя URL профиля
        else:
            messages.error(request, "Неверный email или пароль.")
    return render(request, 'users/login.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})