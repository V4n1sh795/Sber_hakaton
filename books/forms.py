from django import forms
from books.models import Book, BookCopy


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'cover_photo']
        widgets = {
            'cover': forms.ImageField(required=False)
        }


class CreateBookCopyForm(forms.ModelForm):
    # Убираем поле book из формы, если книга уже выбрана
    def __init__(self, *args, **kwargs):
        self.book_id = kwargs.pop('book_id', None)
        super().__init__(*args, **kwargs)
        
        # Если книга передана через URL, скрываем поле выбора книги
        if self.book_id:
            del self.fields['book']
    
    class Meta:
        model = BookCopy
        fields = ['book', 'book_condition_photo']
        widgets = {
            'book': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'book': 'Книга *',
            'book_condition_photo': 'Фото состояния'
        }

class UpdateBookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['book_condition_photo']
        widgets = {
            'book_condition_photo': forms.ImageField(required=True)
        }

class BookFilterListForm(forms.Form):
    title = forms.CharField(
        required=False,
        label='Название',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название книги...'
        })
    )

    genre = forms.ChoiceField(
        choices=[],
        required=False,
        label='Жанр',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'onchange': 'this.form.submit()'
        })
    )
    
    author = forms.ChoiceField(
        choices=[],
        required=False, 
        label='Автор',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'onchange': 'this.form.submit()'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Динамически заполняем choices из базы данных
        genres = Book.objects.values_list('genre', flat=True).distinct().order_by('genre')
        authors = Book.objects.values_list('author', flat=True).distinct().order_by('author')
        
        self.fields['genre'].choices = [('', 'Все жанры')] + [(g, g) for g in genres if g]
        self.fields['author'].choices = [('', 'Все авторы')] + [(a, a) for a in authors if a]