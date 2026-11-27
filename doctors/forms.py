from django import forms
<<<<<<< HEAD:appointments/forms.py
from .models import Appointment

class AppointmentForms(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['comment']
        widgets = {'comment': forms.Textarea(attrs={'placeholder': 'Describe your complaint', 'rows': 3})}

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) > 500:
            raise forms.ValidationError('Comment is too long')
        return comment
=======
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Doctor, Specialization, Service

User = get_user_model()


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxSelectMultiple):
                continue
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'


class DoctorForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user', 'specialization', 'services', 'photo', 'description', 'is_active']
        labels = {'user': 'Пользователь', 'specialization': 'Специализация', 'services': 'Услуги', 'photo': 'Фото', 'description': 'Описание', 'is_active': 'Активен'}
        widgets = {'services': forms.CheckboxSelectMultiple, 'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание врача...'}),}

    def save(self, commit=True):
        doctor = super().save(commit=commit)
        if doctor.user.role != 'doctor':
            doctor.user.role = 'doctor'
            doctor.user.save(update_fields=['role'])
        return doctor


class SpecializationForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['name']


class ServiceForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']
>>>>>>> 60d96f0dff25c3000af12edd9a1275ba9b4e0b14:doctors/forms.py
