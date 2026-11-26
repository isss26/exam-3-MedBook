from datetime import date
from django import forms
from .models import TimeSlot


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['date', 'start_time', 'end_time']

    def clean_date(self):
        d = self.cleaned_data['date']
        if d < date.today():
            raise forms.ValidationError('Нельзя создать слот в прошлом')
        return d

    def clean(self):
        cleaned = super().clean()

        start = cleaned.get('start_time')
        end = cleaned.get('end_time')

        if start and end and start >= end:
            raise forms.ValidationError('Начало должно быть раньше конца')

        return cleaned