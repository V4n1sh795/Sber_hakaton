from django.urls import path
from rentals import views

app_name = 'rentals'

urlpatterns = [
    # Список бронирований для стафа
    path('staff/list/', views.RentalListStaffView.as_view(), name='staff_rental_list'),
    
    # Действия с бронированиями (только для стафа)
    path('staff/<int:pk>/confirm/', views.ConfirmRentalView.as_view(), name='confirm_rental'),
    path('staff/<int:pk>/cancel/', views.CancelRentalView.as_view(), name='cancel_rental'),
    path('staff/<int:pk>/issue/', views.IssueRentalView.as_view(), name='issue_rental'),
    path('staff/<int:pk>/return/', views.ReturnRentalView.as_view(), name='return_rental'),
    
    # Создание бронирования (для пользователей)
    path('create/<int:book_id>/', views.CreateRentalView.as_view(), name='create_rental'),
]
