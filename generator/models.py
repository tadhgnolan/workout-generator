from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Workout(models.Model):
    """
    The body part for the workout: eg: legs, shoulders, arms, back, chest, core
    """
    BODY_PARTS = (
        (0, "legs"),
        (1, "arms"),

    )

    body_part = models.IntergerField(choices = BODY_PARTS, default=0)
    muscle_group = models.CharField(max_length=25, null=False, blank=False)

    def __str__(self):
        return self.body_part


class Exercise(models.Model):
    """
    The exercise that would be generated at random each time.
    """
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    wiki_link = models.URLField(max_length=256, null=False, blank=False)
    sets = models.PositiveIntegerField(
        default=3,
        validators=[MinValueValidator(3), MaxValueValidator(6)],
        null=False, blank=False)
    reps = models.PositiveIntegerField(
        default=12,
        validators=[MinValueValidator(12), MaxValueValidator(20)],
        null=False, blank=False)
    muscle_focus = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name
