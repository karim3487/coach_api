from django.urls import path

from apps.api.v1.progress import views

urlpatterns = [
    path("", views.ProgressListView.as_view(), name="progress-list"),
    path(
        "by-telegram/",
        views.ProgressByTelegramView.as_view(),
        name="progress-by-telegram",
    ),
    path("", views.ProgressCreateView.as_view(), name="progress-create"),
]
