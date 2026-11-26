from django import forms
from .models import Doctor, Specialization, Service


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user', 'specialization', 'services', 'photo', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание врача...'}),}


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['name']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']