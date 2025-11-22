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
    class Meta:
        model = BookCopy
        fields = ['book', 'book_condition_photo']
        widgets = {
            'book_condition_photo': forms.ImageField(required=True)
        }

class UpdateBookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['book_condition_photo']
        widgets = {
            'book_condition_photo': forms.ImageField(required=True)
        }