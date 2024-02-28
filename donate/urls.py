from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_view, name='donation_view'),
    # path(
    #     'cache_donate_data/', views.cache_donate_data, name='cache_donate_data'
    # ),
    path(
        'donation_success/<order_number>',
        views.donation_success,
        name='donation_success'
    ),
]
