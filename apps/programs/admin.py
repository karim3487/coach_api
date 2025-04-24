from django.contrib import admin

from .models import Program, ProgramWorkout


class ProgramWorkoutInline(admin.TabularInline):
    model = ProgramWorkout
    extra = 1


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "goal",
        "level",
        "days_per_week",
        "duration_weeks",
        "location_type",
        "active",
    )
    list_filter = ("goal", "level", "location_type", "active")
    search_fields = ("name",)
    inlines = [ProgramWorkoutInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProgramWorkout)
class ProgramWorkoutAdmin(admin.ModelAdmin):
    list_display = ("program", "workout", "week_number", "day_number")
    list_filter = ("program",)
