from django import forms

class DonationForm(forms.Form):
    amount = forms.DecimalField(max_digits=6, decimal_places=2, max_value=5, min_value=5)
