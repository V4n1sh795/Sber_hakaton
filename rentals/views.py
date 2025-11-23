from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from rentals.forms import CreateRentalForm
from rentals.models import Rental
from books.models import Book, BookCopy

class CreateRentalView(LoginRequiredMixin, CreateView):
    model = Rental
    form_class = CreateRentalForm
    template_name = "create_rental.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['book_id'] = self.kwargs.get('book_id')
        return kwargs
    
    def get_success_url(self):
        messages.success(self.request, f'Книга "{self.object.book.book.title}" успешно забронирована!')
        return reverse_lazy('books:BookFullInfoView', kwargs={'pk': self.object.book.book.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('book_id')
        
        if book_id:
            book = get_object_or_404(Book, pk=book_id)
            context['selected_book'] = book
            
            # Получаем информацию о доступных экземплярах
            available_copies = BookCopy.objects.filter(
                book=book
            ).filter(
                rental__isnull=True, rental__return_date__isnull=False
            ).distinct()
            
            context['available_copies_count'] = available_copies.count()
            context['page_title'] = f'Бронирование: {book.title}'
        else:
            context['page_title'] = 'Бронирование книги'
        
        context['current_user'] = self.request.user
        
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Дополнительная логика после успешного создания
        return response