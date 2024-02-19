from django.contrib import admin
from .models import Workout, Exercise


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_part')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout', 'muscle_focus', 'sets', 'reps')
