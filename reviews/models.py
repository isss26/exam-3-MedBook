from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class DoctorReview(models.Model):
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.CASCADE, related_name='review')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)