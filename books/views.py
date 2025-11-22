from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from books.models import Book, BookCopy
from books.forms import CreateBookForm, BookFilterListForm
from books.forms import CreateBookCopyForm, UpdateBookCopyForm

# Запросы для книг

class CreateBookView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = "books/create_form.html"
    success_url = reverse_lazy('books:BookPagedView')

    def form_valid(self, form):
        # TODO: file size validation
        # TODO: create thumbnail
        response = super().form_valid(form)
        messages.success(self.request, f'Книга "{self.object.title}" успешно создана!')
        return response

# сервисный метод
def get_book_entity_by_id(book_id: int) -> Book:
    return Book.objects.get(id=book_id)

class BookInfoView(DetailView):
    model = Book
    template_name = 'books/info.html'
    context_object_name = 'book'

class BookFullInfoView(DetailView):
    model = Book
    template_name = 'books/full_info.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        book_copy_count = BookCopy.objects.filter(book=book).count()
        context['book_copy_amount'] = book_copy_count
        return context

class BookPagedView(ListView):
    model = Book
    template_name = 'books/list.html'
    context_object_name = 'books'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        
        title = self.request.GET.get('title')
        genre = self.request.GET.get('genre')
        author = self.request.GET.get('author')
        
        # Применяем фильтры
        if title:
            # Поиск по частичному совпадению в названии
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre=genre)
        if author:
            queryset = queryset.filter(author=author)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Добавляем форму фильтрации в контекст
        filter_form = BookFilterListForm(self.request.GET)
        context['filter_form'] = filter_form
        
        # Добавляем информацию о текущих фильтрах
        context['active_filters'] = {
            'title': self.request.GET.get('title'),
            'genre': self.request.GET.get('genre'),
            'author': self.request.GET.get('author'),
        }
        
        return context

# Запросы для экземпляров книг

class CreateBookCopyView(CreateView):
    model = BookCopy
    form_class = CreateBookCopyForm
    template_name = "bookcopies/create_form.html"

    def get_success_url(self):
        messages.success(self.request, 'Экземпляр книги успешно создан!')
        # Убеждаемся, что объект существует и у него есть книга
        if hasattr(self, 'object') and self.object and self.object.book:
            return reverse_lazy('books:BookFullInfoView', kwargs={'pk': self.object.book.pk})
        else:
            # Fallback на список книг, если что-то пошло не так
            return reverse_lazy('books:BookPagedView')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        book_id = self.kwargs.get('book_id')
        print('get_form_kwargs:', book_id)
        if book_id:
            kwargs['initial'] = {'book': book_id}
            kwargs['book_id'] = book_id
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('book_id')
        
        if book_id:
            book = get_book_entity_by_id(book_id)  # Используем get_object_or_404 вместо вашей функции
            context['selected_book'] = book
        
        print('get selected book:', context['selected_book'])

        context['page_title'] = 'Добавить экземпляр книги'
        
        return context
    
    def form_valid(self, form):
        book_id = self.kwargs.get('book_id')
        if book_id:
            book = get_book_entity_by_id(book_id)
            form.instance.book = book
        
        print('form valid:', form.instance.book)

        # Проверяем, что книга установлена
        if not form.instance.book:
            form.add_error('book', 'Необходимо выбрать книгу')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        return response

class UpdateBookCopyView(UpdateView):
    model = BookCopy
    form_class = UpdateBookCopyForm
    template_name = "bookcopies/update_form.html"
    context_object_name = 'book_copy'
    
    def get_success_url(self):
        messages.success(self.request, 'Фото состояния успешно обновлено!')
        return reverse_lazy('books:BookFullInfoView', kwargs={'pk': self.object.book.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        # Можно добавить дополнительную логику перед сохранением
        response = super().form_valid(form)
        return response

class BookCopyInfo(DetailView):
    model = BookCopy
    template_name = 'bookcopies/book_copy_info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_copy = self.object
        book = get_book_entity_by_id(book_copy.book)
        
        # Дополнительная проверка прав доступа
        if not self.request.user.is_authenticated:
            # Лучше использовать декоратор или миксин для проверки прав
            pass

        context['title'] = book.title
        context['author'] = book.author
        context['genre'] = book.genre
        context['condition_photo']=book_copy.book_condition_photo

        return context
    
    def dispatch(self, request, *args, **kwargs):
        # TODO: Проверка прав доступа
        return super().dispatch(request, *args, **kwargs)
