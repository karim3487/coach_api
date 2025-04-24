from django.contrib import admin

from .models import Workout, WorkoutExercise


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "goal", "level", "duration_est", "active")
    list_filter = ("category", "goal", "level", "active")
    search_fields = ("name",)
    inlines = [WorkoutExerciseInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ("workout", "exercise", "order", "sets", "reps", "duration")
    list_filter = ("workout",)
