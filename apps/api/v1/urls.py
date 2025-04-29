from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # drf-spectacular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "schema/docs/",
        SpectacularSwaggerView.as_view(url_name="v1:schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="v1:schema"),
        name="redoc",
    ),
    # My routes
    path("profiles/", include("apps.api.v1.profiles.urls")),
    path("goals/", include("apps.api.v1.goals.urls")),
    path("backup-codes/", include("apps.api.v1.backup_codes.urls")),
    path("exercises/", include("apps.api.v1.exercises.urls")),
    path("plans/", include("apps.api.v1.plans.urls")),
    path("programs/", include("apps.api.v1.programs.urls")),
    path("", include("apps.api.v1.workouts.urls")),  # workouts
]
