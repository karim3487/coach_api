from django.db import models
from django.utils.text import slugify

from apps.common.choices import DifficultyLevel, ExerciseType
from apps.common.models import TimeStampedModel
from apps.exercises.models import Exercise


class Workout(TimeStampedModel):
    name = models.CharField(max_length=100, help_text="Name of the workout session")
    slug = models.SlugField(max_length=100, unique=True)
    category = models.CharField(
        max_length=20,
        choices=ExerciseType.choices,
        help_text="Main type of the workout: strength, cardio, etc.",
    )
    description = models.TextField(help_text="Short summary of the workout session")
    duration_est = models.PositiveIntegerField(
        help_text="Estimated duration in minutes"
    )
    goal = models.ForeignKey(
        "profiles.Goal",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Goal this workout targets (optional)",
    )
    level = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        help_text="Recommended experience level for this workout",
    )
    active = models.BooleanField(
        default=True, help_text="If unchecked, this workout is archived"
    )

    class Meta:
        verbose_name = "Workout"
        verbose_name_plural = "Workouts"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} – {self.category} - {self.level}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        help_text="Workout session this exercise belongs to",
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, help_text="Reference to the base exercise"
    )
    sets = models.PositiveIntegerField(
        null=True, blank=True, help_text="Number of sets (for strength exercises)"
    )
    reps = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of reps per set (for strength exercises)",
    )
    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration in seconds (for cardio/stretching exercises)",
    )
    rest_interval = models.PositiveIntegerField(
        null=True, blank=True, help_text="Rest time in seconds after this exercise"
    )
    order = models.PositiveIntegerField(help_text="Execution order within the workout")
    notes = models.TextField(
        blank=True, help_text="Optional notes or tips for this exercise"
    )

    class Meta:
        verbose_name = "Workout Exercise"
        verbose_name_plural = "Workout Exercises"
        ordering = ["workout", "order"]

    def __str__(self):
        return f"{self.workout} - {self.exercise}"
