from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib import messages
from django.urls import reverse_lazy

from books.models import Book, BookCopy
from books.forms import CreateBookForm
from books.forms import CreateBookCopyForm, UpdateBookCopyForm

# Запросы для книг

class CreateBookView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = "books/create_form.html"
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Книга "{self.object.title}" успешно создана!')
        return response

# сервисный метод
def get_book_entity_by_id(book_id: int) -> Book:
    return Book.objects.filter(id = book_id)

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

# Запросы для экземпляров книг

class CreateBookCopyView(CreateView):
    model = BookCopy
    form_class = CreateBookCopyForm
    template_name = "bookcopies/create_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Экземпляр книги успешно создан!')
        return response

class UpdateBookCopyView(UpdateView):
    model = BookCopy
    form_class = UpdateBookCopyForm
    template_name = "bookcopies/update_form.html"
    success_message_template = 'Экземпляр книги успешно обновлён!'

    def get_success_url(self):
        messages.success(self.request, 'Экземпляр книги успешно обновлён!')
        return reverse_lazy('book_copy_info', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Для UpdateView нужно передать instance
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

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
