from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from .forms import NewsletterForm
import requests

def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
