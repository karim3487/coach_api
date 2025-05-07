from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from apps.api.v1.progress import serializers
from apps.plans.models import Progress


@extend_schema(responses=serializers.ProgressSerializer(many=True))
class ProgressListView(generics.ListAPIView):
    queryset = Progress.objects.all()
    serializer_class = serializers.ProgressSerializer


@extend_schema(
    request=serializers.ProgressSerializer, responses=serializers.ProgressSerializer
)
class ProgressCreateView(generics.CreateAPIView):
    queryset = Progress.objects.all()
    serializer_class = serializers.ProgressSerializer


@extend_schema(
    request=serializers.ProgressCreateByTelegramSerializer,
    responses=serializers.ProgressSerializer,
    description="Create a progress record using telegram_id instead of profile_id.",
)
class ProgressCreateByTelegramView(generics.CreateAPIView):
    queryset = Progress.objects.all()
    serializer_class = serializers.ProgressCreateByTelegramSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        progress_instance = serializer.save()

        output_serializer = serializers.ProgressSerializer(progress_instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
