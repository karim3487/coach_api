from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView

from apps.api.v1.programs import serializers
from apps.programs.models import Program


@extend_schema(
    parameters=[
        OpenApiParameter(name="goal", description="Goal ID", required=False, type=int),
        OpenApiParameter(
            name="level", description="Difficulty level", required=False, type=str
        ),
        OpenApiParameter(
            name="location_type", description="Location type", required=False, type=str
        ),
    ],
    responses={200: serializers.ProgramSerializer(many=True)},
    description="List available training programs with optional filters.",
)
class ProgramListView(generics.ListAPIView):
    serializer_class = serializers.ProgramSerializer
    queryset = Program.objects.filter(active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["goal", "level", "location_type"]


@extend_schema(
    description="Retrieve a program by its slug.",
    responses={200: serializers.ProgramDetailSerializer},
)
class ProgramRetrieveView(RetrieveAPIView):
    queryset = Program.objects.filter(active=True)
    serializer_class = serializers.ProgramDetailSerializer
    lookup_field = "slug"
