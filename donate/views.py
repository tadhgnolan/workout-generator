from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def donation_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            amount_in_cents = int(amount * 100)
            charge = stripe.Charge.create(
                amount=amount_in_cents,
                currency='eur',
                description='Donation',
                source=request.POST['stripeToken']
            )
            donation = Donation(amount=amount)
            donation.save()
            return HttpResponseRedirect(reverse('success'))
    else:
        form = DonationForm()
    return render(request, 'donation.html', {'form': form, 'publishable_key': setting.STRIPE_PUBLISHABLE_KEY})
