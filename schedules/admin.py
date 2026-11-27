from django.contrib import admin
from .models import TimeSlot

# Register your models here.

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'is_booked']
    list_filter = ['is_booked', 'date', 'doctor__specialization']
    search_fields = ['doctor__user__username', 'doctor__user__first_name', 'doctor__user__last_name']