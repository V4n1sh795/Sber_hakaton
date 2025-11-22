from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView
from django.db import IntegrityError

from favorites.models import Favorite
from books.models import Book


@login_required
def add_to_favorites(request, book_id):
    """
    Добавление книги в избранное
    """
    book = get_object_or_404(Book, id=book_id)
    
    try:
        Favorite.objects.create(user=request.user, book=book)
        messages.success(request, f'Книга "{book.title}" добавлена в избранное!')
    except IntegrityError:
        messages.warning(request, f'Книга "{book.title}" уже в избранном!')
    
    # Возвращаемся на предыдущую страницу
    return redirect(request.META.get('HTTP_REFERER', 'books:BookPagedView'))


@login_required
def remove_from_favorites(request, book_id):
    """
    Удаление книги из избранного
    """
    book = get_object_or_404(Book, id=book_id)
    favorite = Favorite.objects.filter(user=request.user, book=book).first()
    
    if favorite:
        favorite.delete()
        messages.success(request, f'Книга "{book.title}" удалена из избранного!')
    else:
        messages.warning(request, f'Книга "{book.title}" не найдена в избранном!')
    
    # Возвращаемся на предыдущую страницу
    return redirect(request.META.get('HTTP_REFERER', 'books:BookPagedView'))


class FavoriteListView(LoginRequiredMixin, ListView):
    """
    Список избранных книг пользователя
    """
    model = Favorite
    template_name = 'favorites/list.html'
    context_object_name = 'favorites'
    paginate_by = 30
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('book')
