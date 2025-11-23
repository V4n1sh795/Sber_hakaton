from django.shortcuts import render
from lib_admin.models import CarouselSlide


def home(request):
    """
    Главная страница
    """
    slides = CarouselSlide.objects.filter(is_active=True)
    return render(request, 'home.html', {'slides': slides})
