from django.db import models


class CarouselSlide(models.Model):
    """Слайды для карусели на главной странице"""
    title = models.CharField('Заголовок', max_length=200)
    image = models.ImageField('Изображение', upload_to='carousel/')
    order = models.PositiveIntegerField('Порядок', default=0, help_text='Порядок отображения слайда')
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Слайд карусели'
        verbose_name_plural = 'Слайды карусели'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
