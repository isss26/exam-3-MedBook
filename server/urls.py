from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doctors/', include('doctors.urls')),
    path('schedules/', include('schedules.urls')),
    path('reviews/', include('reviews.urls'))
]
