from django.db import models


class PlanStatus(models.TextChoices):
    ACTIVE = "active", "Активный"
    COMPLETED = "completed", "Выполнен"
    CANCELLED = "cancelled", "Отменен"
