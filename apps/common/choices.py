from django.db import models


class ExerciseType(models.TextChoices):
    STRENGTH = "strength", "Strength"
    CARDIO = "cardio", "Cardio"
    STRETCHING = "stretching", "Stretching"
    YOGA = "yoga", "Yoga"
    MIXED = "mixed", "Mixed"


class DifficultyLevel(models.TextChoices):
    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"


class TrainingLocation(models.TextChoices):
    GYM = "gym", "Gym"
    HOME = "home", "Home"
    OUTDOORS = "outdoors", "Outdoors"
