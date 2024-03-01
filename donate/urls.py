from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_view, name='donation_view'),
    path(
        'donation_success/<str:order_number>',
        views.donation_success,
        name='donation_success'
    ),
]
