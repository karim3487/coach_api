from django.contrib import admin

from apps.common.admin import DeletedAtFilter, SoftDeleteAdmin
from apps.profiles.models import *


@admin.register(ClientProfile)
class ClientProfileAdmin(SoftDeleteAdmin):
    list_display = (
        "name",
        "age",
        "goal",
        "training_location",
        "created_at",
        "is_deleted",
    )
    list_filter = ("goal", "training_location", "gender", DeletedAtFilter)
    search_fields = ("name",)


@admin.register(Goal)
class GoalAdmin(SoftDeleteAdmin):
    list_display = ("name", "is_deleted")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TelegramID)
class TelegramIDAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "profile")
    search_fields = ("telegram_id", "profile__name")


@admin.register(BackupCode)
class BackupCodeAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "code_hash",
        "used_at",
    )
    list_filter = ("used_at",)
    search_fields = ("profile__name",)
    readonly_fields = ("used_at",)
