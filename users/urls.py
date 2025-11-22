from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', views.autorization_page, name='auth'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('rec/', views.recomendations, name='rec')
]