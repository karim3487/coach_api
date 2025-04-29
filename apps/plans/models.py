from django.db import models

from apps.common.models import TimeStampedModel
from apps.plans.choices import PlanStatus


class Plan(TimeStampedModel):
    client_profile = models.ForeignKey(
        "profiles.ClientProfile",
        on_delete=models.CASCADE,
        help_text="Profile assigned to this training plan",
    )
    program = models.ForeignKey(
        "programs.Program",
        null=True,
        on_delete=models.SET_NULL,
        help_text="Base program used for generating the plan (optional)",
    )
    goal = models.ForeignKey(
        "profiles.Goal",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Goal at the time of plan generation",
    )
    start_date = models.DateField(help_text="Start date of the plan")
    end_date = models.DateField(help_text="End date of the plan")
    status = models.CharField(
        max_length=20,
        choices=PlanStatus.choices,
        default=PlanStatus.ACTIVE,
        help_text="Plan status: active, completed, or cancelled",
    )
    progress_percent = models.PositiveIntegerField(
        default=0, help_text="Completion progress in percentage"
    )

    class Meta:
        verbose_name = "Training Plan"
        verbose_name_plural = "Training Plans"
        ordering = ["-start_date"]

    def mark_completed(self):
        self.status = PlanStatus.COMPLETED
        self.save(update_fields=["status"])

    def cancel(self):
        self.status = PlanStatus.CANCELLED
        self.save(update_fields=["status"])

    def __str__(self):
        return (
            f"{self.client_profile.name}'s Plan ({self.start_date} – {self.end_date})"
        )


class Schedule(TimeStampedModel):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        help_text="Training plan this schedule entry belongs to",
    )
    date = models.DateField(help_text="Scheduled date of the workout")
    time = models.TimeField(help_text="Scheduled time for the workout")
    workout = models.ForeignKey(
        "workouts.Workout",
        null=True,
        on_delete=models.SET_NULL,
        help_text="Workout session assigned to this date",
    )
    day_number = models.PositiveIntegerField(
        help_text="Sequential number of workout in the plan"
    )
    completed = models.BooleanField(
        default=False, help_text="Was the workout completed?"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp when workout was completed"
    )
    notes = models.TextField(blank=True, help_text="Optional user notes or feedback")

    class Meta:
        verbose_name = "Schedule Entry"
        verbose_name_plural = "Schedule"
        ordering = ["date", "time"]
        unique_together = [("plan", "date")]

    def __str__(self):
        return f"{self.plan.client_profile.name} - {self.date} at {self.time}"


class Progress(TimeStampedModel):
    client_profile = models.ForeignKey(
        "profiles.ClientProfile",
        on_delete=models.CASCADE,
        help_text="User this progress entry belongs to",
    )
    date = models.DateField(help_text="Date of progress record")
    plan = models.ForeignKey(
        Plan,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Related training plan (optional)",
    )
    workout = models.ForeignKey(
        "workouts.Workout",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Workout this progress is related to (optional)",
    )
    exercise = models.ForeignKey(
        "exercises.Exercise",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Specific exercise this metric is for (optional)",
    )
    metric = models.CharField(
        max_length=50, help_text="Type of metric: weight, reps, time, bodyfat, etc."
    )
    value = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Value of the metric"
    )
    units = models.CharField(
        max_length=20, help_text="Units of the metric (e.g. kg, %, min, reps)"
    )
    notes = models.TextField(blank=True, help_text="Additional info or context")

    class Meta:
        verbose_name = "Progress Record"
        verbose_name_plural = "Progress Records"
        ordering = ["-date"]

    def __str__(self):
        return (
            f"{self.client_profile.name} - {self.metric}: "
            f"{self.value} {self.units} on {self.date}"
        )
