from django.urls import path
from .views import register_view, confirm_email, login_view, logout_view, profile, change_password

urlpatterns = [
    path('register/', register_view, name='register'),
    path('confirm_email/<uidb64>/<token>/', confirm_email, name='confirm_email'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('change_password/', change_password, name='change_password'),
]
