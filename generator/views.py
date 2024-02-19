import random
from django.shortcuts import render
from .models import Exercise, Workout


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
        # print(body_part[0])  # prints 0, 1, 2, 3, etc.
        # print(body_part[1])  # prints arm, leg, chest, etc.
        # print("------")  # spacer only for testing

        # filter workouts by each unique body part
        body_part_workouts = list(
            exercises.filter(workout=body_part[0])
        )
        # grab a random workout using this body_part
        random_workout = random.sample(body_part_workouts, 1)
        # append it to the list generated to the user
        generated_workout.append(random_workout)

    template = "generator/generator.html"
    context = {
        "generated_workout": generated_workout,
    }
    return render(request, template, context)