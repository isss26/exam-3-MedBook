from datetime import datetime
from django import forms
from django.utils import timezone
from doctors.forms import BootstrapMixin
from .models import TimeSlot


class TimeSlotForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['date', 'start_time', 'end_time']
        labels = {'date': 'Дата', 'start_time': 'Начало', 'end_time': 'Конец'}
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'start_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

    def __init__(self, *args, doctor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.doctor = doctor

    def clean_date(self):
        d = self.cleaned_data['date']
        if d < timezone.localdate():
            raise forms.ValidationError('Нельзя создать слот в прошлом')
        return d

    def clean(self):
        cleaned = super().clean()

        d = cleaned.get('date')
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')

        if not (d and start and end):
            return cleaned

        if start >= end:
            raise forms.ValidationError('Начало должно быть раньше конца')

        if timezone.make_aware(datetime.combine(d, start)) <= timezone.now():
            raise forms.ValidationError('Это время уже прошло')

        if TimeSlot.objects.filter(doctor=self.doctor, date=d, start_time__lt=end, end_time__gt=start).exists():
            raise forms.ValidationError('У вас уже есть слот на это время')

        return cleaned