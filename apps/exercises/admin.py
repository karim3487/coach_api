from django.contrib import admin
from django.contrib.postgres.search import (
    TrigramSimilarity,
)
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            queryset = (
                queryset.annotate(
                    similarity=TrigramSimilarity("name", search_term),
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )
        return queryset, use_distinct

    def media_preview(self, obj):
        if obj.media_url:
            return format_html(
                '<img src="{}" width="100" style="object-fit: contain;" />',
                obj.media_url,
            )
        return "-"

    media_preview.short_description = "Preview"
