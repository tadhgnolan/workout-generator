from django.shortcuts import render
from .models import SignupModel

def signup_view(request):
    signup = SignupModel.objects.get(title='Sign Up For Newsletter')
    return render(request, 'signup.html', {'signup': signup})
