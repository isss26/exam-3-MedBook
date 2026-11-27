from django.contrib import admin
from .models import Appointment, AppointmentHistory

# Register your models here.

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'slot', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['patient__username']

admin.site.register(AppointmentHistory)