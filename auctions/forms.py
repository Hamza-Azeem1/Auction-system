from django.forms import ModelForm
from django import forms
from .models import Listing
from django.utils import timezone

class ListingForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and start_time < timezone.now():
            self.add_error('start_time', 'Start time must be the current time.')

        if start_time and end_time and start_time >= end_time:
            self.add_error('end_time', 'End time must be greater than the start time.')

        return cleaned_data

    class Meta:
        model = Listing
        fields = ['name', 'initial', 'category', 'image', 'description', 'start_time', 'end_time']
