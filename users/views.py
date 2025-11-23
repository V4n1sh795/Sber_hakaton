
# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from rentals.models import Rental
from books.models import Book, BookCopy
from .forms import StaffUserCreationForm
import users.rec as rec


def is_staff_or_admin(user):
    """Проверка, что пользователь - сотрудник или администратор"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


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
            if user.is_superuser:
                return redirect('/admin/')  # Админ-панель для staff и superuser
            else:
                return redirect('/')  # Личный кабинет для обычных пользователей
        else:
            messages.error(request, "Неверный email или пароль.")
    
    return render(request, 'users/login.html')


@login_required
def profile_view(request):
    """
    Профиль пользователя
    """
    from django.utils import timezone
    
    # Активные выдачи (книги не возвращены)
    active_rentals = Rental.objects.filter(
        user=request.user,
        return_date__isnull=True
    ).select_related('book')
    
    # История выдач (книги возвращены)
    history_rentals = Rental.objects.filter(
        user=request.user,
        return_date__isnull=False
    ).select_related('book').order_by('-return_date')[:10]
    
    # Уведомления о просроченных книгах
    notifications = []
    today = timezone.now().date()
    for rental in active_rentals:
        if rental.borrow_date:
            days_passed = (today - rental.borrow_date).days
            if days_passed > 30:  # Книга должна быть возвращена через 30 дней
                notifications.append(f"{rental.book.title} — просрочено")
    
    context = {
        'user': request.user,
        'active_rentals': active_rentals,
        'history_rentals': history_rentals,
        'notifications': notifications,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def logout_view(request):
    """
    Выход из системы (только POST для безопасности)
    """
    from django.contrib.auth import logout
    
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Вы успешно вышли из системы.")
        return redirect('users:login')
    
    # Если GET - показываем страницу подтверждения
    return render(request, 'users/logout_confirm.html')
@login_required
def recomendations(request):
    if request.method == 'GET':
        user = request.user  # или любой объект пользователя

        # Получаем все записи аренды пользователя
        # rentals = user.rental_set.all()
        # КОД НИЖЕ УДАЛИТЬ НА ПРОДЕ
        # ВОТ ДО СЮДА
        # Получаем только книги (без дубликатов)
        books = Book.objects.filter(bookcopy__rental__user=user).distinct()
        print(books)
        res = []
        for book in books:
            res.append(rec.recommend(book.title))
        res = [book for sublist in res for book in sublist]
        print(res)
        return render(request, 'users/recomedation.html', {'books': res})


@user_passes_test(is_staff_or_admin, login_url='/users/login/')
def register_user_view(request):
    """
    Регистрация нового пользователя сотрудником или администратором.
    Доступно только для staff и superuser.
    """
    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.get_generated_password()
            messages.success(
                request,
                f'Пользователь {user.full_name} ({user.email}) успешно создан. '
                f'Пароль: {password}'
            )
            return redirect('users:register_user')  # Можно изменить на другую страницу
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = StaffUserCreationForm()
    
    return render(request, 'users/register_user.html', {'form': form})
    