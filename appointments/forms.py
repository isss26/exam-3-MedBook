from django import forms
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