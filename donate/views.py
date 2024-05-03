from django.shortcuts import get_object_or_404, render, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import DonationForm
from .models import Donation

import stripe


@require_POST
def cache_donate_data(request):
    try:
        amount = request.POST.get('amount')
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'amount': amount,
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed right now. '
            'Please try again later.'
        )
        return HttpResponse(content=e, status=400)


def donation_view(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe_currency = settings.STRIPE_CURRENCY

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation_amount = int(float(request.POST.get('amount')) * 100)
            pid = request.POST.get('client_secret').split('_secret')[0]
            donation.stripe_product_id = pid
            donation.save()

            # update the PaymentIntent
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=donation_amount,
                currency=stripe_currency,
            )

            return HttpResponseRedirect(
                reverse('donation_success', args=[donation.order_number]))
        else:
            messages.error(request, form.errors)
    else:
        stripe_total = round(5 * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=stripe_currency,
        )
        form = DonationForm()

    template = 'donate/donation.html'
    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if intent else None,
    }
    return render(request, template, context)


def donation_success(request, order_number):
    """
    Handle successful donations
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Donation, order_number=order_number)
    messages.success(
        request,
        'Donation successfully processed! '
        f'Your donation order number is {order.order_number}. '
        f'A confirmation email will be sent to {order.email}.'
    )

    customer_email = order.email
    contact_email = settings.DEFAULT_FROM_EMAIL
    subject = "Workout Generator Donation Confirmation"
    body = render_to_string(
        'donate/confirmation_emails/confirmation_email_body.txt',
        {'donation': order, 'contact_email': contact_email}
    )
    send_mail(
        subject,
        body,
        contact_email,
        [customer_email]
    )

    template = 'donate/donation_success.html'
    context = {
        'donation': order,
    }

    return render(request, template, context)
