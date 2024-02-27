from django.urls import path
from . import views

urlpatterns = [
    path('', views.donate, name='donation'),
    path('donation_success/<order_number>', views.donation_success, name='donation_success'),
]
