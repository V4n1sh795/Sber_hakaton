from django import forms
from .models import Event
from django.utils import timezone


class EventForm(forms.ModelForm):
    """
    Форма для создания и редактирования событий (только для staff/admin)
    """
    
    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'description', 'event_photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Встреча с автором'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Опишите событие подробнее...'
            }),
            'event_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'name': 'Название события *',
            'start_date': 'Дата и время начала *',
            'end_date': 'Дата и время окончания *',
            'description': 'Описание',
            'event_photo': 'Фото события'
        }
    
    def clean_start_date(self):
        """Проверка, что дата начала не в прошлом"""
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < timezone.now():
            raise forms.ValidationError('Дата начала события не может быть в прошлом.')
        return start_date
    
    def clean(self):
        """Проверка, что дата окончания позже даты начала"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError('Дата окончания должна быть позже даты начала.')
        
        return cleaned_data
    
    def clean_name(self):
        """Валидация названия"""
        name = self.cleaned_data.get('name')
        if name and len(name) < 5:
            raise forms.ValidationError('Название должно содержать минимум 5 символов.')
        return name