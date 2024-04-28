from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Newsletter
from .forms import NewsletterForm


def newsletter(request):
    newsletter_form = NewsletterForm(request.POST or None)
    if request.method == "POST":
        email = request.POST.get("email")

        if newsletter_form.is_valid():
            # check if the email already exists in the database
            if Newsletter.objects.filter(email=email).exists():
                messages.error(
                    request,
                    "Your email is already registered for our newsletter."
                )
            else:
                newsletter_form.save()
                messages.success(
                    request, "Thanks for signing up to our newsletter!"
                )

                # send newsletter confirmation email
                contact_email = settings.DEFAULT_FROM_EMAIL
                subject = "Workout Generator Newsletter Confirmation"
                body = (
                    f"Thanks for signing up to our newsletter, {email}!\n"
                    "We'll let you know when there are new Workouts\n"
                    "and Exercises available on our site.\n\n"
                    "- The Workout Generator Team"
                )
                send_mail(
                    subject,
                    body,
                    contact_email,
                    [email]
                )

                return redirect("newsletter")

    template = "newsletter/newsletter.html"
    context = {
        "newsletter_form": newsletter_form,
    }
    return render(request, template, context)
