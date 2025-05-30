from rest_framework.routers import DefaultRouter

from apps.api.v1.workouts import views

router = DefaultRouter()
router.register("", views.WorkoutViewSet, basename="workout")

urlpatterns = router.urls
