from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import DonationForm
from .models import Donation
import stripe


def donation_view(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

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
            return HttpResponseRedirect(reverse('donation_success', args=[donation.order_number]))
    else:
        stripe_total = round(5 * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        form = DonationForm()
    template = 'donate/donation.html'
    context = {
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)


def donation_success(request, order_number):
    """
    Handle successful donations
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Donation successfully processed! \
        Your donation order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    
    customer_email = order.email
    contact_email = settings.DEFAULT_FROM_EMAIL
    subject = "Workout Generator Donation Confirmation"
    body = {
        "Thank you for donating to Workout Generator. \n"
        "Please find your donation order details below. \n\n"
        "Order Number: {order.order_number} \n"
    }