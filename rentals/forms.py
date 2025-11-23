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
            # Получаем все экземпляры конкретной книги
            all_copies = BookCopy.objects.filter(book_id=self.book_id)
        else:
            # Получаем все экземпляры
            all_copies = BookCopy.objects.all()
        
        # Фильтруем только те, у которых НЕТ активной аренды
        # Активная аренда = return_date is NULL
        available_copies = []
        for copy in all_copies:
            has_active_rental = Rental.objects.filter(
                book=copy,
                return_date__isnull=True  # Книга не возвращена
            ).exists()
            
            if not has_active_rental:
                available_copies.append(copy)
        
        return available_copies
    
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