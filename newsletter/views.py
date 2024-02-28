from django.shortcuts import render
from .models import signup

def signup(request):
    signup = Signup.objects.get(title='Sign Up For Newsletter')
    return render(request, 'signup.html', {'signup': signup})
