from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookPagedView.as_view(), name='BookPagedView'),
    path('<int:pk>/', views.BookFullInfoView.as_view(), name='BookFullInfoView'),
]
