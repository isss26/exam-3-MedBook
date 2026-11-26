from django.urls import path
from . import views
app_name = 'reviews'

urlpatterns = [
    path('appointment/<int:appointment_id>/create/', views.review_create, name='review_create'),
    path('<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('<int:pk>/delete/', views.review_delete, name='review_delete'),
    
    
    
]