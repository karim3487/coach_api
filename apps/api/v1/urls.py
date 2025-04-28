from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # drf-spectacular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("profiles/", include("apps.api.v1.profiles.urls")),
    path("goals/", include("apps.api.v1.goals.urls")),
    path("backup-codes/", include("apps.api.v1.backup_codes.urls")),
    path("exercises/", include("apps.api.v1.exercises.urls")),
    path("", include("apps.api.v1.workouts.urls")),
]
