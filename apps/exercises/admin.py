from django.contrib import admin
from django.utils.html import format_html

from apps.exercises.models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "muscle_group",
        "equipment",
        "difficulty",
        "media_preview",
    )
    list_filter = ("type", "muscle_group", "equipment", "difficulty")
    search_fields = ("name",)
    list_editable = ("type", "muscle_group", "equipment", "difficulty")

    def media_preview(self, obj):
        if obj.media_url:
            return format_html(
                '<img src="{}" width="100" style="object-fit: contain;" />',
                obj.media_url,
            )
        return "-"

    media_preview.short_description = "Preview"
