from django.shortcuts import (
    render, reverse, redirect,
    get_object_or_404, HttpResponse
)
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import DonationForm
from .models import Donation
import stripe


@require_POST
def cache_donate_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed right now. '
            'Please try again later.'
        )
        return HttpResponse(content=e, status=400)


def donation(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form_data = {
            'amount': request.POST['amount'],
            'email': request.POST['email'],
        }

        donation_form = DonationForm(form_data)
        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            donation.stripe_product_id = pid
            donation.save()
            return redirect(
                reverse('donation_success', args=[donation.order_number])
            )
        else:
            messages.error(
                request,
                'There was an error with your form. '
                'Please double check your information.'
            )
    else:
        stripe_total = round(5 * 100)  # each donation is €5.00
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        print(intent)

        # Attempt to prefill the form with logged-in user email
        if request.user.is_authenticated:
            donation_form = DonationForm(initial={'email': request.user.email})
        else:
            donation_form = DonationForm()

    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing. '
            'Did you forget to set it in your environment?'
        )

    template = 'donate/donation.html'
    context = {
        'form': donation_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def donation_success(request, order_number):
    """
    Handle successful donation_success
    """
    donation = get_object_or_404(Donation, order_number=order_number)
    messages.success(
        request,
        'Thank you for your donation! '
        'Your card was charged €5.00.'
        f'A confirmation email will be sent to {donation.email}.'
    )

    # Send the user a confirmation email
    cust_email = donation.email
    subject = f"Donation Payment for €{donation.amount}"
    body = render_to_string(
        'donate/confirmation_emails/confirmation_email_body.txt',
        {'donation': donation, 'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )

    template = 'donate/donation_success.html'
    context = {
        'donation': donation,
    }

    return render(request, template, context)