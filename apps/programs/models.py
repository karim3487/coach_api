from django.db import models
from django.utils.text import slugify

from apps.common.choices import DifficultyLevel, TrainingLocation
from apps.workouts.models import Workout


class Program(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the training program")
    slug = models.SlugField(max_length=100, unique=True)
    goal = models.ForeignKey(
        "profiles.Goal",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Main fitness goal this program targets",
    )
    description = models.TextField(
        help_text="Description of the program structure and focus"
    )
    days_per_week = models.PositiveIntegerField(
        help_text="Number of training days per week"
    )
    duration_weeks = models.PositiveIntegerField(
        help_text="Total duration of the program in weeks"
    )
    level = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        help_text="Difficulty level (e.g., beginner, intermediate, advanced)",
    )
    location_type = models.CharField(
        max_length=20,
        choices=TrainingLocation.choices,
        help_text="Preferred training location (e.g., gym, home, any)",
    )
    active = models.BooleanField(
        default=True, help_text="Is this program currently active and assignable?"
    )

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.goal.name if self.goal else 'No goal'})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProgramWorkout(models.Model):
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, help_text="Program this workout is part of"
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        help_text="Workout session assigned to the program",
    )
    day_number = models.PositiveIntegerField(
        help_text="Day number in weekly cycle "
        "(e.g., 1 = first training day of the week)"
    )
    week_number = models.PositiveIntegerField(
        default=1,
        help_text="Week number in the program cycle"
        " (default is 1 for recurring weekly plans)",
    )

    class Meta:
        verbose_name = "Program Workout"
        verbose_name_plural = "Program Workouts"
        ordering = ["program", "week_number", "day_number"]
        unique_together = [("program", "week_number", "day_number")]

    def __str__(self):
        return f"{self.program.name} - Week {self.week_number}, Day {self.day_number}"
