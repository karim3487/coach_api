from django.contrib import admin

from apps.common.admin import DeletedAtFilter, SoftDeleteAdmin
from apps.workouts.models import Workout, WorkoutExercise


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1


@admin.register(Workout)
class WorkoutAdmin(SoftDeleteAdmin):
    list_display = ("name", "category", "goal", "level", "duration_est", "active")
    list_filter = ("category", "goal", "level", "active", DeletedAtFilter)
    search_fields = ("name",)
    inlines = [WorkoutExerciseInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ("workout", "exercise", "order", "sets", "reps", "duration")
    list_filter = ("workout",)
