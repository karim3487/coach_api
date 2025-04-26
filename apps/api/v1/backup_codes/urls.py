from django.urls import path

from apps.api.v1.backup_codes import views

urlpatterns = [
    path(
        "generate/",
        views.GenerateBackupCodesView.as_view(),
        name="generate-backup-codes",
    ),
    path("use/", views.UseBackupCodeView.as_view(), name="use-backup-code"),
]
