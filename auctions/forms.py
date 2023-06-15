from django.forms import ModelForm
from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'})
    )

    class Meta:
        model = Listing
        fields = ['name', 'initial', 'category', 'image', 'description', 'start_time', 'end_time']
