from django import forms
from django.core.validators import MinValueValidator
from .models import Donation


class DonationForm(forms.ModelForm):
    amount = forms.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Donation
        fields = ("amount", "email")
