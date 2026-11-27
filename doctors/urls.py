from django.urls import path
from . import views
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
    
    
]