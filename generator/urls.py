from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.generator, name='generator'),
    path('add_workout/', views.add_workout, name='add_workout'),
    path('edit_workout/<int:id>/', views.edit_workout, name='edit_workout'),
    path(
        'delete_workout/<int:id>/',
        views.delete_workout, name='delete_workout'),
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    path('edit_exercise/<int:id>/', views.edit_exercise, name='edit_exercise'),
    path(
        'delete_exercise/<int:id>/',
        views.delete_exercise, name='delete_exercise'),
]
