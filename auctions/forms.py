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

class PaymentForm(forms.Form):
    cardholder_name = forms.CharField(label='Cardholder Name', max_length=100)
    card_number = forms.CharField(label='Card Number', max_length=16, min_length=16)
    expiry_month = forms.IntegerField(label='Expiry Month', min_value=1, max_value=12)
    expiry_year = forms.IntegerField(label='Expiry Year', min_value=2023)  # Assuming current year is 2023
    cvc = forms.CharField(label='CVC', max_length=4, min_length=3)
    iban_number = forms.CharField(label='IBAN Number', max_length=34)

    def clean_cardholder_name(self):
        cardholder_name = self.cleaned_data['cardholder_name']
        if not cardholder_name.isalpha():
            raise forms.ValidationError("Name should contain only Alphabets.")
        return cardholder_name

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.isdigit():
            raise forms.ValidationError("Card number should contain only digits.")
        return card_number

    def clean_expiry_month(self):
        expiry_month = self.cleaned_data['expiry_month']
        if expiry_month < 1 or expiry_month > 12:
            raise forms.ValidationError("Expiry month should be between 1 and 12.")
        return expiry_month

    def clean_expiry_year(self):
        expiry_year = self.cleaned_data['expiry_year']
        if expiry_year < 2023:  # Assuming current year is 2023
            raise forms.ValidationError("Expiry year should be the current year or later.")
        return expiry_year

    def clean_cvc(self):
        cvc = self.cleaned_data['cvc']
        if not cvc.isdigit():
            raise forms.ValidationError("CVC should contain only digits.")
        return cvc

    def clean_iban_number(self):
        iban_number = self.cleaned_data['iban_number']
        if not iban_number.replace(' ', '').isalnum():
            raise forms.ValidationError("IBAN number should contain only alphanumeric characters.")
        return iban_number

