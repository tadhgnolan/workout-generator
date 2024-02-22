import random
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Exercise, Workout
from .forms import ExerciseForm, WorkoutForm


def generator(request):
    """
    Generate a workout regime.
    Grab a workout/exercise from each muscle group.
    """
    # get all workouts
    workouts = Workout.objects.all()
    # get all exercises
    exercises = Exercise.objects.all()
    # set an empty list of workouts to display to user
    generated_workout = []

    # list of each body part
    for body_part in Workout.BODY_PARTS:
        # filter workouts by each unique body part
        body_part_list = list(
            exercises.filter(workout__body_part=body_part[0])
        )
        # grab a random workout using this body_part
        random_workout = random.sample(body_part_list, 1)
        # append it to the list generated to the user
        generated_workout.append(random_workout)

    template = "generator/generator.html"
    context = {
        "generated_workout": generated_workout,
    }
    return render(request, template, context)


def add_workout(request):
    """ Admin-only page to add new workouts """
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin-only access")
        return redirect(reverse("generator"))

    workout_form = WorkoutForm(request.POST or None)
    if request.method == "POST":
        if workout_form.is_valid():
            workout_form.save()
            messages.success(request, "Workout added!")
            return redirect(reverse("generator"))
        messages.error(request, "Error, try again.")

    template = "generator/add_workout.html"
    context = {
        "workout_form": workout_form,
    }
    return render(request, template, context)


def edit_workout(request, id):
    """ Admin-only page to edit workouts """
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin-only access")
        return redirect(reverse("generator"))

    workout = get_object_or_404(Workout, id=id)
    workout_form = WorkoutForm(request.POST or None, instance=workout)
    if request.method == "POST":
        if workout_form.is_valid():
            workout_form.save()
            messages.success(request, "Workout updated!")
            return redirect(reverse("generator"))
        messages.error(request, "Error, try again.")

    template = "generator/edit_workout.html"
    context = {
        "workout": workout,
        "workout_form": workout_form,
    }
    return render(request, template, context)


def delete_workout(request, id):
    """ Admin-only page to delete workouts """
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin-only access")
        return redirect(reverse("generator"))

    workout = get_object_or_404(Workout, id=id)
    workout.delete()
    messages.success(request, "Workout updated!")
    return redirect(reverse("generator"))
