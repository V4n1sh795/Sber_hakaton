from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('auth/', views.autorization_page, name='auth'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]