from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='doctors:doctor_list'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('doctors/', include('doctors.urls')),
    path('schedules/', include('schedules.urls')),
    path('reviews/', include('reviews.urls')),
    path('appointments/', include('appointments.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)