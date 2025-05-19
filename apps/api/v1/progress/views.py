from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.progress import serializers
from apps.common.pagination import CustomPagination
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


class ProgressByTelegramView(APIView):
    pagination_class = CustomPagination

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
        responses=serializers.ProgressSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        telegram_id = request.query_params.get("telegram_id")
        profile = get_object_or_404(
            ClientProfile, telegram_ids__telegram_id=telegram_id
        )
        queryset = Progress.objects.filter(client_profile=profile).order_by("-date")
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        serializer = serializers.ProgressSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=serializers.ProgressCreateByTelegramSerializer,
        responses=serializers.ProgressSerializer,
        description="Create a progress record using telegram_id instead of profile_id.",
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.ProgressCreateByTelegramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        progress_instance = serializer.save()

        output_serializer = serializers.ProgressSerializer(progress_instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
