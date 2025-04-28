from rest_framework.routers import DefaultRouter

from apps.api.v1.exercises import views

router = DefaultRouter()
router.register("", views.ExerciseViewSet, basename="exercise")

urlpatterns = router.urls
