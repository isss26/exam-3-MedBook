from django.contrib import admin
from .models import Specialization, Service, Doctor

# Register your models here.

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'specialization', 'is_active']
    list_filter = ['is_active', 'specialization', 'services']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    filter_horizontal = ['services']