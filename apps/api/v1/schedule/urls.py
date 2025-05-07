from django.urls import path

from apps.api.v1.schedule import views

urlpatterns = [
    path("", views.ScheduleListView.as_view(), name="schedule-list"),
    path("<int:pk>/", views.ScheduleRetrieveView.as_view(), name="schedule-detail"),
    path(
        "complete-today/",
        views.ScheduleCompleteView.as_view(),
        name="schedule-complete",
    ),
    path(
        "today-workout/<int:telegram_id>",
        views.GetTodayWorkoutView.as_view(),
        name="today-workout",
    ),
    path(
        "today-schedule/<int:telegram_id>",
        views.GetTodayScheduleView.as_view(),
        name="today-schedule",
    ),
    path(
        "by-telegram/",
        views.ScheduleListByTelegramView.as_view(),
        name="schedule-by-telegram",
    ),
]
