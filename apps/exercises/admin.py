from django.contrib import admin

from apps.exercises.models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "muscle_group", "equipment", "difficulty")
    list_filter = ("type", "muscle_group", "equipment", "difficulty")
    search_fields = ("name",)
