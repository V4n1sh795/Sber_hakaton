from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    # path('logout/', views.logout_view, name='logout'),
    path('auth/', views.register_user, name='auth'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout')
    # path('auth/send_auth/', views.register_user, name="registaraion")
]