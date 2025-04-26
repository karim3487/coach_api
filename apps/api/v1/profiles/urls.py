from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.api.v1.profiles import views

router = DefaultRouter()
router.register("", views.ClientProfileViewSet, basename="clientprofile")

urlpatterns = router.urls

urlpatterns += [
    path(
        "by-telegram/<int:telegram_id>/",
        views.ClientProfileByTelegramView.as_view(),
        name="profile-by-telegram",
    ),
]
