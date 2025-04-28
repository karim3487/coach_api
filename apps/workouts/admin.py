from django.contrib import admin
from django.utils.html import format_html

from apps.common.admin import DeletedAtFilter, SoftDeleteAdmin
from apps.workouts.models import Workout, WorkoutExercise


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1
    # autocomplete_fields = ("exercise",)
    raw_id_fields = ("exercise",)
    readonly_fields = ("exercise_preview",)
    fields = (
        "exercise_preview",
        "exercise",
        "sets",
        "reps",
        "duration",
        "rest_interval",
        "order",
        "notes",
    )
    classes = ("wide",)

    def exercise_preview(self, obj):
        if obj.exercise and obj.exercise.media_url:
            return format_html(
                '<div style="display: flex; align-items: center;">'
                '<img src="{}" width="120" height="120" '
                'style="object-fit: contain; border: 1px solid #ccc; margin: 5px;" />'
                "</div>",
                obj.exercise.media_url,
            )
        return format_html(
            '<div style="width: 120px; height: 120px; border: 1px dashed #ccc; margin: 5px;"></div>'  # noqa: E501
        )

    exercise_preview.short_description = "Упражнение (GIF)"

    class Media:
        css = {"all": ("admin/custom_admin.css",)}


@admin.register(Workout)
class WorkoutAdmin(SoftDeleteAdmin):
    list_display = ("name", "category", "goal", "level", "duration_est", "active")
    list_filter = ("category", "goal", "level", "active", DeletedAtFilter)
    search_fields = ("name",)
    inlines = [WorkoutExerciseInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        # "exercise",
        "workout",
    )
    raw_id_fields = ("exercise",)
    list_display = ("workout", "exercise", "order", "sets", "reps", "duration")
    list_filter = ("workout",)
    readonly_fields = ("exercise_preview",)

    def exercise_preview(self, obj):
        """HTML для превью гифки."""
        if obj.exercise and obj.exercise.media_url:
            return format_html(
                '<img id="exercise-preview-img" src="{}" width="300" style="object-fit: contain;" />',  # noqa: E501
                obj.exercise.media_url,
            )
        return format_html(
            '<img id="exercise-preview-img" src="" width="300" style="object-fit: contain; display: none;" />'  # noqa: E501
        )

    exercise_preview.short_description = "Preview GIF"
