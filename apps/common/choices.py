from django.db import models


class ExerciseType(models.TextChoices):
    STRENGTH = "strength", "Сила"
    CARDIO = "cardio", "Кардио"
    STRETCHING = "stretching", "Растяжка"
    YOGA = "yoga", "Йога"
    MIXED = "mixed", "Смешанное"


class DifficultyLevel(models.TextChoices):
    BEGINNER = "beginner", "Новичок"
    INTERMEDIATE = "intermediate", "Средний"
    ADVANCED = "advanced", "Продвинутый"


class TrainingLocation(models.TextChoices):
    GYM = "gym", "Зал"
    HOME = "home", "Дом"
    OUTDOORS = "outdoors", "Улица"
