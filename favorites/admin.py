from django.contrib import admin
from favorites.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'id')
    list_filter = ('user',)
    search_fields = ('user__email', 'user__name', 'user__lastname', 'book__title', 'book__author')
    raw_id_fields = ('user', 'book')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'book')

