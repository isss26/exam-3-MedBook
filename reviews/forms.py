from django import forms
from doctors.forms import BootstrapMixin
from .models import DoctorReview


class DoctorReviewForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = DoctorReview
        fields = ['rating', 'text']
        labels = {'rating': 'Оценка', 'text': 'Отзыв'}
        widgets = {
            'rating': forms.Select(choices=[(1, '1 звезда'), (2, '2 звезды'), (3, '3 звезды'), (4, '4 звезды'), (5, '5 звёзд'),]),
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите свой отзыв...'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']

        if rating < 1 or rating > 5:
            raise forms.ValidationError('Рейтинг должен быть от 1 до 5')

        return rating