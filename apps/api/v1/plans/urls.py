from django.urls import path

from apps.api.v1.plans import views

urlpatterns = [
    # Read
    path("", views.PlanListView.as_view(), name="plan-list"),
    path("<int:pk>/", views.PlanRetrieveView.as_view(), name="plan-detail"),
    path(
        "current/by-telegram/<int:telegram_id>/",
        views.CurrentPlanByTelegramView.as_view(),
        name="plan-current-by-telegram",
    ),
    # Create with AI
    path(
        "create/ai/by-profile/",
        views.CreateAIPlanByProfileView.as_view(),
        name="plan-create-ai-by-profile",
    ),
    path(
        "create/ai/by-telegram/",
        views.CreateAIPlanByTelegramView.as_view(),
        name="plan-create-ai-by-telegram",
    ),
    # Create from program
    path(
        "create/from-program/by-profile/",
        views.CreatePlanFromProgramByProfileView.as_view(),
        name="plan-create-from-program-by-profile",
    ),
    path(
        "create/from-program/by-telegram/",
        views.CreatePlanFromProgramByTelegramView.as_view(),
        name="plan-create-from-program-by-telegram",
    ),
]
