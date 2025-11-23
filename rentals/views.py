from django.views.generic import CreateView, ListView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from rentals.forms import CreateRentalForm
from rentals.models import Rental
from books.models import Book, BookCopy


class StaffRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь является стафом"""
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет доступа к этой странице. Требуются права сотрудника.')
        return redirect('home')


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
            # Экземпляры доступны если:
            # 1. Никогда не арендовались (rental__isnull=True)
            # 2. ИЛИ все их аренды имеют return_date (книга возвращена)
            all_copies = BookCopy.objects.filter(book=book)
            
            # Находим занятые экземпляры (есть аренда без return_date И статус issued)
            occupied_copy_ids = Rental.objects.filter(
                book__book=book,
                status__in=['pending', 'confirmed', 'issued']  # Занят если в процессе бронирования или выдан
            ).values_list('book_id', flat=True)
            
            # Доступные = все минус занятые
            available_copies = all_copies.exclude(id__in=occupied_copy_ids)
            
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


class RentalListStaffView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Список всех бронирований для стафа"""
    model = Rental
    template_name = 'rentals/rental_list_staff.html'
    context_object_name = 'rentals'
    paginate_by = 20
    
    def get_queryset(self):
        from django.db.models import Count, Q
        
        queryset = Rental.objects.select_related('book__book', 'user').annotate(
            user_rental_count=Count(
                'user__rental',
                filter=Q(user__rental__status__in=['pending', 'confirmed', 'issued']),
                distinct=True
            )
        ).all()
        
        # Фильтрация по статусу
        status = self.request.GET.get('status')
        if status and status in dict(Rental.STATUS_CHOICES):
            queryset = queryset.filter(status=status)
        
        # Поиск по пользователю
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                user__email__icontains=search
            ) | queryset.filter(
                user__name__icontains=search
            ) | queryset.filter(
                user__lastname__icontains=search
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Rental.STATUS_CHOICES
        context['current_status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Статистика
        context['stats'] = {
            'pending': Rental.objects.filter(status='pending').count(),
            'confirmed': Rental.objects.filter(status='confirmed').count(),
            'issued': Rental.objects.filter(status='issued').count(),
            'returned': Rental.objects.filter(status='returned').count(),
            'cancelled': Rental.objects.filter(status='cancelled').count(),
        }
        
        return context


class ConfirmRentalView(LoginRequiredMixin, StaffRequiredMixin, View):
    """Подтверждение бронирования"""
    def post(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        
        if rental.status != 'pending':
            messages.warning(request, f'Бронь #{rental.pk} уже имеет статус "{rental.get_status_display()}"')
        else:
            rental.confirm()
            messages.success(request, f'Бронь #{rental.pk} успешно подтверждена!')
        
        return redirect('rentals:staff_rental_list')


class CancelRentalView(LoginRequiredMixin, StaffRequiredMixin, View):
    """Отмена бронирования"""
    def post(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        
        if rental.status == 'cancelled':
            messages.warning(request, f'Бронь #{rental.pk} уже отменена')
        elif rental.status == 'issued':
            messages.error(request, f'Невозможно отменить бронь #{rental.pk}, так как книга уже выдана')
        else:
            rental.cancel()
            messages.success(request, f'Бронь #{rental.pk} отменена')
        
        return redirect('rentals:staff_rental_list')


class IssueRentalView(LoginRequiredMixin, StaffRequiredMixin, View):
    """Выдача книги (перевод в статус issued)"""
    def post(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        
        if rental.status == 'cancelled':
            messages.error(request, f'Невозможно выдать книгу по отмененной брони #{rental.pk}')
        elif rental.status == 'issued':
            messages.warning(request, f'Книга по брони #{rental.pk} уже выдана')
        else:
            rental.issue()
            messages.success(request, f'Книга по брони #{rental.pk} выдана пользователю!')
        
        return redirect('rentals:staff_rental_list')


class ReturnRentalView(LoginRequiredMixin, StaffRequiredMixin, View):
    """Возврат книги (перевод в статус returned)"""
    def post(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        
        if rental.status == 'cancelled':
            messages.error(request, f'Невозможно вернуть книгу по отмененной брони #{rental.pk}')
        elif rental.status == 'returned':
            messages.warning(request, f'Книга по брони #{rental.pk} уже возвращена')
        elif rental.status != 'issued':
            messages.error(request, f'Книга по брони #{rental.pk} еще не была выдана')
        else:
            rental.return_book()
            messages.success(request, f'Книга по брони #{rental.pk} успешно возвращена!')
        
        return redirect('rentals:staff_rental_list')