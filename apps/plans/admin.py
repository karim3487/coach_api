from django.contrib import admin

from .models import Plan, Progress, Schedule


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "client_profile",
        "program",
        "goal",
        "start_date",
        "end_date",
        "status",
        "progress_percent",
    )
    list_filter = ("status", "goal", "program")
    search_fields = ("client_profile__name",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("plan", "date", "time", "workout", "completed")
    list_filter = ("completed", "date", "workout")
    search_fields = ("plan__client_profile__name",)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("client_profile", "date", "metric", "value", "units")
    list_filter = ("metric", "date")
    search_fields = ("client_profile__name", "metric")
