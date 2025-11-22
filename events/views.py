from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event


def event_list(request):
    """
    Список событий с пагинацией
    """
    events = Event.objects.all().order_by('-date')
    
    # Пагинация - 10 событий на страницу
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'events': page_obj.object_list,
    }
    
    return render(request, 'events/event_list.html', context)


def event_detail(request, event_id):
    """
    Детальная страница события
    """
    event = get_object_or_404(Event, pk=event_id)
    
    context = {
        'event': event,
    }
    
    return render(request, 'events/event_detail.html', context)
