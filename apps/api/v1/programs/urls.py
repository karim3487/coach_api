from django.urls import path

from apps.api.v1.programs.views import ProgramListView, ProgramRetrieveView

urlpatterns = [
    path("", ProgramListView.as_view(), name="program-list"),
    path("<slug:slug>/", ProgramRetrieveView.as_view(), name="program-detail"),
]
