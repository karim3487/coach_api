from django.contrib import admin

from apps.common.admin import DeletedAtFilter, SoftDeleteAdmin, TimeStampedAdmin
from apps.programs.models import Program, ProgramWorkout


class ProgramWorkoutInline(admin.TabularInline):
    readonly_fields = [
        "deleted_at",
    ]
    model = ProgramWorkout
    extra = 1


@admin.register(Program)
class ProgramAdmin(SoftDeleteAdmin):
    list_display = (
        "name",
        "goal",
        "level",
        "days_per_week",
        "duration_weeks",
        "location_type",
        "active",
    )
    list_filter = ("goal", "level", "location_type", "active", DeletedAtFilter)
    search_fields = ("name",)
    inlines = [ProgramWorkoutInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProgramWorkout)
class ProgramWorkoutAdmin(SoftDeleteAdmin, TimeStampedAdmin):
    list_display = ("program", "workout", "week_number", "day_number")
    list_filter = ("program", DeletedAtFilter)
