from rest_framework.routers import DefaultRouter

from apps.api.v1.profiles.views import ClientProfileViewSet

router = DefaultRouter()
router.register("", ClientProfileViewSet, basename="clientprofile")

urlpatterns = router.urls
