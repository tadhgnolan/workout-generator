from django import forms
from .models import Workout, Exercise


class WorkoutForm(forms.ModelForm):
    """ Form to allow admins to manage Workouts. """
    class Meta:
        model = Workout
        fields = "__all__"


class ExerciseForm(forms.ModelForm):
    """ Form to allow admins to manage Exercise. """
    class Meta:
        model = Exercise
        fields = "__all__"
