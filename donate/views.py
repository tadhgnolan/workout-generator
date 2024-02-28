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
    return render(request, 'donation.html', {'form': form, 'public_key': setting.STRIPE_PUBLIC_KEY})


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