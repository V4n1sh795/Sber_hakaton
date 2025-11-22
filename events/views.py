from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event
from .forms import EventForm


def is_staff_or_superuser(user):
    """Проверка: является ли пользователь staff или superuser"""
    return user.is_staff or user.is_superuser


def event_list(request):
    """
    Список событий с пагинацией (доступен всем)
    """
    events = Event.objects.all().order_by('-date')
    
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
    
    # Можно добавить связанные отзывы
    # reviews = event.reviewevent_set.all()
    
    context = {
        'event': event,
        # 'reviews': reviews,
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
