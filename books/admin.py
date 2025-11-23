from django.contrib import admin
from django.utils.safestring import mark_safe
from books.models import Book, BookCopy


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'genre', 'has_cover', 'copies_count']
    list_filter = ['genre', 'author']
    search_fields = ['title', 'author', 'genre', 'description']
    readonly_fields = ['cover_thumbnail_preview', 'cover_photo_preview']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'genre', 'description')
        }),
        ('Обложка книги', {
            'fields': ('cover_photo', 'cover_photo_preview', 'cover_thumbnail_preview'),
            'description': 'Загрузите обложку книги. Превью создастся автоматически.'
        }),
    )
    
    def has_cover(self, obj):
        return bool(obj.cover_photo)
    has_cover.short_description = 'Обложка'
    has_cover.boolean = True
    
    def copies_count(self, obj):
        count = BookCopy.objects.filter(book=obj).count()
        return f'{count} шт.'
    copies_count.short_description = 'Экземпляров'
    
    def cover_photo_preview(self, obj):
        if obj.cover_photo:
            return mark_safe(f'<img src="{obj.cover_photo.url}" style="max-height: 300px; max-width: 300px;" />')
        return 'Нет изображения'
    cover_photo_preview.short_description = 'Превью полной обложки'
    
    def cover_thumbnail_preview(self, obj):
        if obj.cover_thumbnail:
            return mark_safe(f'<img src="{obj.cover_thumbnail.url}" style="max-height: 200px; max-width: 200px;" />')
        return 'Нет превью'
    cover_thumbnail_preview.short_description = 'Превью миниатюры'
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Создаем thumbnail если загружена обложка
        if obj.cover_photo and not obj.cover_thumbnail:
            obj.create_thumbnail()
    
    actions = ['generate_thumbnails']
    
    def generate_thumbnails(self, request, queryset):
        updated = 0
        for book in queryset:
            if book.cover_photo and not book.cover_thumbnail:
                book.create_thumbnail()
                updated += 1
        self.message_user(request, f'Создано превью для {updated} книг(и)')
    generate_thumbnails.short_description = 'Создать превью для выбранных книг'


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_title', 'book_author', 'has_condition_photo', 'registered_at', 'rental_status']
    list_filter = ['registered_at', 'book__genre', 'book__author']
    search_fields = ['book__title', 'book__author']
    readonly_fields = ['registered_at', 'updated_at', 'condition_photo_preview']
    autocomplete_fields = ['book']
    
    fieldsets = (
        ('Связь с книгой', {
            'fields': ('book',)
        }),
        ('Фото состояния', {
            'fields': ('book_condition_photo', 'condition_photo_preview'),
            'description': 'Загрузите фото текущего состояния экземпляра книги'
        }),
        ('Временные метки', {
            'fields': ('registered_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Название книги'
    book_title.admin_order_field = 'book__title'
    
    def book_author(self, obj):
        return obj.book.author
    book_author.short_description = 'Автор'
    book_author.admin_order_field = 'book__author'
    
    def has_condition_photo(self, obj):
        return bool(obj.book_condition_photo)
    has_condition_photo.short_description = 'Фото состояния'
    has_condition_photo.boolean = True
    
    def rental_status(self, obj):
        from rentals.models import Rental
        rentals = Rental.objects.filter(book=obj, return_date__isnull=True)
        if rentals.exists():
            rental = rentals.first()
            return f'В аренде ({rental.get_status_display()})'
        return 'Доступен'
    rental_status.short_description = 'Статус аренды'
    
    def condition_photo_preview(self, obj):
        if obj.book_condition_photo:
            return mark_safe(f'<img src="{obj.book_condition_photo.url}" style="max-height: 300px; max-width: 300px;" />')
        return 'Нет фото'
    condition_photo_preview.short_description = 'Превью фото состояния'
