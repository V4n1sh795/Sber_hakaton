from io import BytesIO
import os
from django.db import models
from PIL import Image
from django.core.files.base import ContentFile


class Book(models.Model):
    """
    Книга
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    genre = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    cover_photo = models.ImageField(
                            upload_to='covers/full/',
                            null=True, 
                            blank=True,
                            verbose_name='Обложка книги',
                            help_text='Загрузите фотографию книги'
                        )
    cover_thumbnail = models.ImageField(
                            upload_to='covers/thumbnails/',
                            null=True, 
                            blank=True,
                            verbose_name='Превью обложки',
                            help_text='Генерируемая превью книги'
    )
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
    
    def __str__(self):
        return f"{self.title} - {self.author}"

    def save(self, *args, **kwargs):
        """Переопределяем save для автоматического создания thumbnail"""
        # Сначала сохраняем объект, чтобы файл был доступен
        super().save(*args, **kwargs)
        
        # Если есть обложка, но нет thumbnail - создаем
        if self.cover_photo and not self.cover_thumbnail:
            self.create_thumbnail()

    def create_thumbnail(self):
        """Создает thumbnail из основного изображения"""
        try:
            # Открываем основное изображение
            img = Image.open(self.cover_photo.path)
            
            # Определяем размеры для thumbnail
            thumbnail_size = (200, 300)
            
            # Конвертируем в RGB если нужно
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Создаем thumbnail
            img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
            
            # Сохраняем в память
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=80)
            thumb_io.seek(0)
            
            # Формируем имя файла
            filename = os.path.basename(self.cover_photo.name)
            name, ext = os.path.splitext(filename)
            thumb_filename = f"{name}_thumb.jpg"
            
            # Сохраняем thumbnail
            self.cover_thumbnail.save(
                thumb_filename,
                ContentFile(thumb_io.getvalue()),
                save=False
            )
            
            # Сохраняем модель
            super().save()
            
        except Exception as e:
            print(f"Ошибка при создании thumbnail: {e}")

class BookCopy(models.Model):
    """
    Экземпляр книги
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_condition_photo = models.ImageField(
                            upload_to='copies/condition/full/',
                            null=True, 
                            blank=True,
                            verbose_name='Фотография состояния книги',
                            help_text='Загрузите фотографию исходного состояния книги'
                        )
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
    
    def __str__(self):
        return f"{self.book.title} (ID: {self.id}, зарегистрирован: {self.registered_at.strftime('%d.%m.%Y')})"