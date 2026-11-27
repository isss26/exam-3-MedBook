from django.urls import path
from . import views
<<<<<<< HEAD:appointments/urls.py

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
=======
app_name = 'doctors'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('create/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('<int:pk>/edit/', views.DoctorUpdateView.as_view(), name='doctor_edit'),
    path('<int:pk>/delete/', views.DoctorDeactivateView.as_view(), name='doctor_delete'),
    path('specializations/', views.SpecializationListView.as_view(), name='specialization_list'),
    path('specializations/create/', views.SpecializationCreateView.as_view(), name='specialization_create'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    
    
>>>>>>> 60d96f0dff25c3000af12edd9a1275ba9b4e0b14:doctors/urls.py
]