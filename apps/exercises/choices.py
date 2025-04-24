from django.db import models


class EquipmentType(models.TextChoices):
    BODYWEIGHT = "bodyweight", "Bodyweight"
    DUMBBELLS = "dumbbells", "Dumbbells"
    BARBELL = "barbell", "Barbell"
    RESISTANCE_BANDS = "resistance_bands", "Resistance Bands"
    KETTLEBELL = "kettlebell", "Kettlebell"
    MACHINE = "machine", "Machine"
    MAT = "mat", "Mat"
    BENCH = "bench", "Bench"
    NONE = "none", "No Equipment"
    OTHER = "other", "Other"


class MuscleGroup(models.TextChoices):
    CHEST = "chest", "Chest"
    BACK = "back", "Back"
    SHOULDERS = "shoulders", "Shoulders"
    ARMS = "arms", "Arms"
    LEGS = "legs", "Legs"
    CORE = "core", "Core"
    FULL_BODY = "full_body", "Full Body"
    CARDIO = "cardio", "Cardiovascular System"
    FLEXIBILITY = "flexibility", "Flexibility / Mobility"
    OTHER = "other", "Other"
