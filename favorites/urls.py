from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('add/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/<int:book_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('', views.FavoriteListView.as_view(), name='list'),
]
