from django.db import models
from django.conf import settings

# Create your models here.


class Appointment(models.Model):
    STATUS_CHOICES = (('pending', 'Pending'), ('confirmed', 'Confirmed'),('completed', 'Completed'), ('cancelled', 'Cancelled'),)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    slot = models.ForeignKey('schedules.TimeSlot', on_delete=models.PROTECT, related_name='appointments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient}--{self.status}'




class AppointmentHistory(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.appointment}--{self.new_status}'