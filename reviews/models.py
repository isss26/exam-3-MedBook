from django.db import models

# Create your models here.

class DoctorReview(models.Model):
    pass
    # appointment	OneToOneField → Appointment
    # author	ForeignKey → User
    # rating	PositiveSmallIntegerField
    # text	TextField
    # created_at	DateTimeField