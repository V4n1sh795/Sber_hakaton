# books/forms.py
from django import forms
from rentals.models import Rental
from books.models import Book, BookCopy
from django.utils import timezone
from datetime import timedelta
import random

class CreateRentalForm(forms.ModelForm):
    borrow_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': timezone.now().date().isoformat()
        }),
        initial=timezone.now().date(),
        label='Дата выдачи *'
    )
    
    expected_return_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': (timezone.now() + timedelta(days=1)).date().isoformat()
        }),
        label='Планируемая дата возврата'
    )

    class Meta:
        model = Rental
        fields = ['book', 'borrow_date', 'expected_return_date']
        
        widgets = {
            'book': forms.HiddenInput(),  # Скрываем поле, так как экземпляр выбирается автоматически
        }
        
        labels = {
            'book': 'Экземпляр книги',
        }
    
    def __init__(self, *args, **kwargs):
        self.book_id = kwargs.pop('book_id', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Находим случайный доступный экземпляр
        available_copies = self.get_available_copies()
        
        if available_copies:
            # Выбираем случайный экземпляр
            random_copy = random.choice(available_copies)
            self.fields['book'].initial = random_copy
        else:
            self.fields['book'].initial = None
    
    def get_available_copies(self):
        """Возвращает список доступных экземпляров книги"""
        from django.db.models import Q
        from datetime import date
        
        if self.book_id:
            # Ищем доступные экземпляры конкретной книги
            available_copies = BookCopy.objects.filter(
                book_id=self.book_id
            ).filter(
                Q(rental__isnull=True) |  # Никогда не арендовались
                Q(rental__return_date__isnull=False) |  # Уже возвращены
                Q(rental__borrow_date__gt=date.today())  # Аренда в будущем
            ).distinct()
        else:
            # Ищем любые доступные экземпляры
            available_copies = BookCopy.objects.filter(
                Q(rental__isnull=True) |
                Q(rental__return_date__isnull=False) |
                Q(rental__borrow_date__gt=date.today())
            ).distinct()
        
        return list(available_copies)
    
    def clean(self):
        cleaned_data = super().clean()
        book_copy = cleaned_data.get('book')
        borrow_date = cleaned_data.get('borrow_date')
        
        if not book_copy:
            raise forms.ValidationError("Нет доступных экземпляров для бронирования")
        
        if book_copy and borrow_date:
            # Проверяем, не арендован ли экземпляр уже на эту дату
            existing_rental = Rental.objects.filter(
                book=book_copy,
                return_date__isnull=True,  # Не возвращена
                borrow_date__lte=borrow_date  # Дата выдачи уже прошла
            ).exists()
            
            if existing_rental:
                raise forms.ValidationError("Этот экземпляр книги уже арендован")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance