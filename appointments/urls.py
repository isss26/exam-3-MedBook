from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('available/<int:doctor_id>/', views.available_slots, name='available_slots'),
    path('book/<int:slot_id>/', views.book_appointment, name='book_appointment'),
    path('my/', views.MyAppointmentsView.as_view(), name='my_appointments'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('doctor/', views.doctor_appointments, name='doctor_appointments'),
    path('<int:pk>/confirm/', views.confirm_appointment, name='confirm_appointment'),
    path('<int:pk>/complete/', views.complete_appointment, name='complete_appointment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    
]