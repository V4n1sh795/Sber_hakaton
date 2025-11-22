from django.urls import path
from .views import add_book, delete_book, add_user, delete_user

urlpatterns = [
    path('admin/books/', add_book, name='add-book'),
    path('admin/books/<int:pk>/', delete_book, name='delete-book'),
    path('admin/users/', add_user, name='add-user'),
    path('admin/users/<int:pk>/', delete_user, name='delete-user'),
]
