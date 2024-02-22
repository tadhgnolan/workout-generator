from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.generator, name='generator'),
    path('add_workout/', views.add_workout, name='add_workout'),
    path('edit_workout/<int:id>/', views.edit_workout, name='edit_workout'),
    path('delete_workout/<int:id>/', views.delete_workout, name='delete_workout'),
]
