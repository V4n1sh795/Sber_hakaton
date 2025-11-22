from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event, EventSubscription
from .forms import EventForm


def is_staff_or_superuser(user):
    """Проверка: является ли пользователь staff или superuser"""
    return user.is_staff or user.is_superuser


def event_list(request):
    """
    Список событий с пагинацией (доступен всем)
    """
    events = Event.objects.all().order_by('-start_date')
    
    # Пагинация - 9 событий на страницу
    paginator = Paginator(events, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'events': page_obj.object_list,
    }
    
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    """
    Детальная страница события (доступна всем)
    """
    event = get_object_or_404(Event, pk=pk)
    
    # Проверка подписки пользователя (если авторизован)
    user_subscription = None
    if request.user.is_authenticated:
        user_subscription = EventSubscription.objects.filter(
            event=event,
            user=request.user,
            status='active'
        ).first()
    
    # Проверка, что событие предстоит в будущем
    event_is_upcoming = event.is_upcoming()
    
    context = {
        'event': event,
        'user_subscription': user_subscription,
        'event_is_upcoming': event_is_upcoming,
    }
    
    return render(request, 'events/event_detail.html', context)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='/users/login/')
def event_create(request):
    """
    Создание нового события (только для staff/admin)
    """
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Событие "{event.name}" успешно создано!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'title': 'Создать событие',
        'button_text': 'Создать'
    }
    
    return render(request, 'events/event_form.html', context)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='/users/login/')
def event_edit(request, pk):
    """
    Редактирование события (только для staff/admin)
    """
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Событие "{event.name}" успешно обновлено!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'title': 'Редактировать событие',
        'button_text': 'Сохранить'
    }
    
    return render(request, 'events/event_form.html', context)


@login_required
@user_passes_test(is_staff_or_superuser, login_url='/users/login/')
def event_delete(request, pk):
    """
    Удаление события (только для staff/admin)
    """
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'Событие "{event_name}" удалено.')
        return redirect('events:list')
    
    context = {
        'event': event,
    }
    
    return render(request, 'events/event_delete_confirm.html', context)


@login_required
def event_subscribe(request, pk):
    """
    Подписка на событие с выбором типа напоминания
    """
    if request.method != 'POST':
        return redirect('events:detail', pk=pk)
    
    event = get_object_or_404(Event, pk=pk)
    
    # Проверяем, что событие ещё не началось
    if not event.is_upcoming():
        messages.error(request, 'Нельзя подписаться на событие, которое уже началось или завершилось.')
        return redirect('events:detail', pk=pk)
    
    # Проверяем, нет ли уже активной подписки
    existing_subscription = EventSubscription.objects.filter(
        event=event,
        user=request.user,
        status='active'
    ).first()
    
    if existing_subscription:
        messages.warning(request, 'Вы уже подписаны на это событие.')
        return redirect('events:detail', pk=pk)
    
    # Получаем тип напоминания из формы
    reminder_type = request.POST.get('reminder_type', 'none')
    
    # Создаём подписку
    subscription = EventSubscription.objects.create(
        event=event,
        user=request.user,
        reminder_type=reminder_type,
        status='active'
    )
    
    messages.success(request, f'Вы успешно подписались на событие "{event.name}".')
    return redirect('events:detail', pk=pk)


@login_required
def event_unsubscribe(request, pk):
    """
    Отписка от события
    """
    if request.method != 'POST':
        return redirect('events:detail', pk=pk)
    
    event = get_object_or_404(Event, pk=pk)
    
    # Ищем активную подписку
    subscription = EventSubscription.objects.filter(
        event=event,
        user=request.user,
        status='active'
    ).first()
    
    if not subscription:
        messages.warning(request, 'Вы не подписаны на это событие.')
        return redirect('events:detail', pk=pk)
    
    # Отменяем подписку
    subscription.status = 'unsubscribed'
    subscription.save()
    
    messages.success(request, f'Вы отписались от события "{event.name}".')
    return redirect('events:detail', pk=pk)
