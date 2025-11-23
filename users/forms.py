from django import forms
from django.utils.crypto import get_random_string
from .models import CustomUser


class StaffUserCreationForm(forms.ModelForm):
    """
    Форма для создания пользователя сотрудником библиотеки или администратором.
    Пароль генерируется автоматически.
    """
    generated_password = forms.CharField(
        label='Сгенерированный пароль',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; font-family: monospace; font-weight: bold;'
        }),
        help_text='Пароль сгенерирован автоматически. Запишите его для передачи пользователю.',
        required=False
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'lastname', 'patronymic', 'phone', 'generated_password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.com'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'patronymic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество (необязательно)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__'
            }),
        }
        labels = {
            'email': 'Email',
            'name': 'Имя',
            'lastname': 'Фамилия',
            'patronymic': 'Отчество',
            'phone': 'Телефон',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Генерируем пароль при создании формы
        if not self.instance.pk:  # Только для новых пользователей
            self.generated_password_value = get_random_string(
                length=12,
                allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
            )
            self.initial['generated_password'] = self.generated_password_value
    
    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    def save(self, commit=True):
        """Сохранение пользователя с установленным паролем"""
        user = super().save(commit=False)
        # Используем сгенерированный пароль
        user.set_password(self.generated_password_value)
        user.username = self.cleaned_data['email']  # username = email
        if commit:
            user.save()
        return user
    
    def get_generated_password(self):
        """Возвращает сгенерированный пароль"""
        return getattr(self, 'generated_password_value', None)
