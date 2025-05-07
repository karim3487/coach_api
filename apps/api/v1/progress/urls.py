from django.urls import path

from apps.api.v1.progress import views

urlpatterns = [
    path("", views.ProgressListView.as_view(), name="progress-list"),
    path("", views.ProgressCreateView.as_view(), name="progress-create"),
    path(
        "by-telegram/",
        views.ProgressCreateByTelegramView.as_view(),
        name="progress-create-by-telegram",
    ),
]
