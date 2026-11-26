from django.conf import settings
from django.db import models

class Specialization(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField('Название', max_length=150, unique=True)
    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor')
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT, related_name='doctors')
    services = models.ManyToManyField(Service, blank=True, related_name='doctors')
    photo = models.ImageField(upload_to='doctors/', blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.user.get_full_name() or self.user.username