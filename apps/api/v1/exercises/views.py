from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from apps.api.v1.common.serializers import PaginatedSerializer
from apps.api.v1.exercises import serializers
from apps.exercises.models import Exercise


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = serializers.ExerciseSerializer

    @extend_schema(responses=PaginatedSerializer)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
