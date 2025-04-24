from django.contrib import admin


class DeletedAtFilter(admin.SimpleListFilter):
    title = "Deleted"
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return [
            ("active", "Active"),
            ("deleted", "Deleted"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "active":
            return queryset.filter(deleted_at__isnull=True)
        elif self.value() == "deleted":
            return queryset.filter(deleted_at__isnull=False)
        return queryset


class TimeStampedAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    list_filter = (("deleted_at", admin.EmptyFieldListFilter),)

    def is_deleted(self, obj):
        return obj.deleted_at is not None

    is_deleted.boolean = True


class SoftDeleteAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    list_filter = (DeletedAtFilter,)

    def is_deleted(self, obj):
        return obj.deleted_at is not None

    is_deleted.boolean = True
    is_deleted.short_description = "Deleted?"
