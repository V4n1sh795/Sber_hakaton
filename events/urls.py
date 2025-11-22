from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='list'),
    path('<int:pk>/', views.event_detail, name='detail'),
    path('create/', views.event_create, name='create'),
    path('<int:pk>/edit/', views.event_edit, name='edit'),
    path('<int:pk>/delete/', views.event_delete, name='delete'),
    path('<int:pk>/subscribe/', views.event_subscribe, name='subscribe'),
    path('<int:pk>/unsubscribe/', views.event_unsubscribe, name='unsubscribe'),
]
