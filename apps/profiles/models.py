from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.common.choices import TrainingLocation
from apps.common.models import TimeStampedModel
from apps.profiles.choices import Contraindication, Gender


class Goal(TimeStampedModel):
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


class ClientProfile(TimeStampedModel):
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
    contraindications = models.CharField(
        blank=True,
        choices=Contraindication.choices,
        help_text="Medical limitations or injuries (free text)",
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

    def __str__(self):
        return f"{self.name} ({self.telegram_ids.count()} tg-ids)"


class TelegramID(models.Model):
    profile = models.ForeignKey(
        "ClientProfile", on_delete=models.CASCADE, related_name="telegram_ids"
    )
    telegram_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"tg:{self.telegram_id} -> {self.profile.name}"


class BackupCode(models.Model):
    profile = models.ForeignKey(
        "ClientProfile", on_delete=models.CASCADE, related_name="backup_codes"
    )
    code_hash = models.CharField(max_length=128, unique=True)
    salt = models.CharField(max_length=32)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile.name} ({self.code_hash[:10]})"

    def is_used(self):
        return self.used_at is not None

    def mark_used(self):
        self.used_at = timezone.now()
        self.save()
