from django.contrib import admin
from .models import Specialization, Service, Doctor

# Register your models here.

admin.site.register([Specialization, Service, Doctor])