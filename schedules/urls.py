from django.urls import path
from . import views
app_name = 'schedules'

urlpatterns = [
    path('doctor/<int:doctor_id>/', views.doctor_schedule, name='doctor_schedule'),
    path('slots/create/', views.slot_create, name='slot_create'),
    path('slots/<int:pk>/delete/', views.slot_delete, name='slot_delete'),
    
    
]