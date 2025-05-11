from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.api.v1.progress import serializers
from apps.api.v1.progress.serializers import ProgressSerializer
from apps.plans.models import Progress
from apps.profiles.models import ClientProfile


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


@extend_schema(
    summary="Get progress by user Telegram ID",
    parameters=[
        OpenApiParameter(
            name="telegram_id",
            description="User Telegram ID",
            required=True,
            type=int,
            location=OpenApiParameter.QUERY,
        )
    ],
    responses=ProgressSerializer(many=True),
)
class ProgressListByTelegramView(generics.ListAPIView):
    serializer_class = serializers.ProgressSerializer

    def get_queryset(self):
        telegram_id = self.request.query_params.get("telegram_id")
        profile = get_object_or_404(
            ClientProfile, telegram_ids__telegram_id=telegram_id
        )
        return Progress.objects.filter(client_profile=profile).order_by("-date")
