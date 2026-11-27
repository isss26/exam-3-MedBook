from django.db import models


class TimeSlot(models.Model):
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'start_time']
        constraints = [models.UniqueConstraint(fields=['doctor', 'date', 'start_time'], name='unique_slot')]

    def __str__(self):
        return f'{self.doctor} {self.date} {self.start_time:%H:%M}-{self.end_time:%H:%M}'