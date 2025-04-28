from django.db import models

from apps.common.choices import DifficultyLevel, ExerciseType
from apps.exercises import choices


class Exercise(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the exercise")
    type = models.CharField(
        max_length=20,
        choices=ExerciseType.choices,
        help_text="Main type: strength, cardio, yoga, etc.",
    )
    muscle_group = models.CharField(
        max_length=50,
        choices=choices.MuscleGroup.choices,
        help_text="Primary muscle group targeted",
    )
    equipment = models.CharField(
        max_length=50,
        choices=choices.EquipmentType.choices,
        help_text="Required equipment for the exercise",
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        help_text="Recommended difficulty level",
    )
    description = models.TextField(
        blank=True, help_text="Instructions and notes about execution"
    )
    media_url = models.URLField(
        blank=True, help_text="Link to a demo video or image (optional)"
    )
    media_file = models.FileField(upload_to="exercises/", null=True, blank=True)

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"
        # ordering = ["name"]
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["muscle_group"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.type}, {self.muscle_group})"
