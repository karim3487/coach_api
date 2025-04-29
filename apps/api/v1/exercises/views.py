# from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from apps.api.v1.exercises import serializers
from apps.exercises.models import Exercise


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = serializers.ExerciseSerializer
