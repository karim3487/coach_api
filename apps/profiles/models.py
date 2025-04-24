from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.common.choices import TrainingLocation
from apps.profiles.choices import Gender


class Goal(models.Model):
    name = models.CharField(
        max_length=50,
        help_text="Name of the fitness goal (e.g. weight loss, muscle gain)",
    )
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(
        blank=True, help_text="Optional description or guidance for the goal"
    )

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ClientProfile(models.Model):
    telegram_id = models.BigIntegerField(
        unique=True, help_text="Telegram chat ID (used for sending notifications)"
    )
    name = models.CharField(max_length=100, help_text="Full name or nickname")
    age = models.PositiveIntegerField(help_text="User's age in years")
    weight = models.DecimalField(
        max_digits=5, decimal_places=1, help_text="Weight in kg"
    )
    height = models.DecimalField(
        max_digits=5, decimal_places=1, help_text="Height in cm"
    )
    gender = models.CharField(
        max_length=10, choices=Gender.choices, help_text="Gender of the user"
    )
    contraindications = models.TextField(
        blank=True, help_text="Medical limitations or injuries (free text)"
    )
    goal = models.ForeignKey(
        "Goal",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Main fitness goal selected by the user",
    )
    training_location = models.CharField(
        max_length=50,
        choices=TrainingLocation.choices,
        help_text="Preferred training location",
    )
    available_days = models.JSONField(
        default=list,
        help_text="List of days user is available for training "
        "(e.g. ['mon', 'wed', 'fri'])",
    )
    preferred_time = models.TimeField(help_text="Preferred daily training time")
    created_at = models.DateTimeField(
        default=timezone.now, help_text="Date of registration"
    )

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["telegram_id"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.telegram_id})"
