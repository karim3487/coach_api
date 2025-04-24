from django.contrib import admin

from apps.profiles.models import *


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "telegram_id",
        "age",
        "goal",
        "training_location",
        "created_at",
    )
    list_filter = ("goal", "training_location", "gender")
    search_fields = ("name", "telegram_id")
    readonly_fields = ("created_at",)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
