from django.contrib import admin
from .models import DoctorReview

# Register your models here.

@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'doctor__specialization']
    search_fields = ['text', 'author__username', 'doctor__user__last_name']