from django.db import models

# Create your models here.

class TimeSlot(models.Model):
    pass
    # doctor	ForeignKey → Doctor
    # date	DateField
    # start_time	TimeField
    # end_time	TimeField
    # is_booked	BooleanField