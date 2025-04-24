from django.contrib import admin

from apps.common.admin import DeletedAtFilter, SoftDeleteAdmin
from apps.plans.models import Plan, Progress, Schedule


@admin.register(Plan)
class PlanAdmin(SoftDeleteAdmin):
    list_display = (
        "client_profile",
        "program",
        "goal",
        "start_date",
        "end_date",
        "status",
        "progress_percent",
    )
    list_filter = ("status", "goal", "program", DeletedAtFilter)
    search_fields = ("client_profile__name",)


@admin.register(Schedule)
class ScheduleAdmin(SoftDeleteAdmin):
    list_display = ("plan", "date", "time", "workout", "completed")
    list_filter = ("completed", "date", "workout", DeletedAtFilter)
    search_fields = ("plan__client_profile__name",)


@admin.register(Progress)
class ProgressAdmin(SoftDeleteAdmin):
    list_display = ("client_profile", "date", "metric", "value", "units")
    list_filter = ("metric", "date", DeletedAtFilter)
    search_fields = ("client_profile__name", "metric")
