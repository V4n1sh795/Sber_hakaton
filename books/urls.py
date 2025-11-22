from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookPagedView.as_view(), name='BookPagedView'),
    path('create/', views.CreateBookView.as_view(), name='CreateBookView'),
    path('<int:pk>/', views.BookFullInfoView.as_view(), name='BookFullInfoView'),
    path('<int:book_id>/create-copy/', views.CreateBookCopyView.as_view(), name='CreateBookCopyView')
]
