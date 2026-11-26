from django.db import models

# Create your models here.

class Specialization(models.Model):
    pass
    # Кардиолог
    # Стоматолог
    # Невролог
    # Хирург



class Service(models.Model):
    pass
    # Консультация
    # УЗИ
    # Анализы


class Doctor(models.Model):
    pass
    # Пользователь (OneToOneField с моделью пользователя участника 2).
    # Специализация (ForeignKey).
    # Услуги (ManyToManyField).
    # Фото (ImageField).
    # Описание.
    # Активность (is_active).