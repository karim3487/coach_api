from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.api.v1.goals import views

router = DefaultRouter()
router.register("", views.GoalViewSet, basename="goal")

urlpatterns = router.urls

urlpatterns += [
    path("by-name/<slug:slug>/", views.GoalBySlugView.as_view(), name="goal-by-slug"),
]
