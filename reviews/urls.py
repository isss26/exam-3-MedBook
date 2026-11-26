from django.urls import path, include
from . import views
app_name = 'reviews'

urlpatterns = [
    path('create/<int:appointment_id>/', views.review_create, name='review_create'),
    path('<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('reviews/', include('reviews.urls')),
    
    
    
]