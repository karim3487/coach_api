from typing import Any

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.profiles import serializers
from apps.api.v1.profiles.serializers import ClientProfileShortSerializer
from apps.profiles import exceptions
from apps.profiles.models import ClientProfile, Goal


class ClientProfileViewSet(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = serializers.ClientProfileSerializer

    def get_serializer_class(self) -> type:
        if self.action == "create":
            return serializers.ClientProfileCreateSerializer
        return super().get_serializer_class()

    @extend_schema(
        request=serializers.ClientProfileCreateSerializer,
        responses={201: serializers.ClientProfileSerializer},
        examples=[
            OpenApiExample(
                name="Create ClientProfile Example",
                value={
                    "name": "Ali",
                    "age": 30,
                    "weight": 75.5,
                    "height": 180.0,
                    "gender": "male",
                    "training_location": "gym",
                    "available_days": ["mon", "wed", "fri"],
                    "preferred_time": "18:00:00",
                    "goal": 1,
                    "telegram_id": 123456789,
                },
                request_only=True,
            )
        ],
    )
    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        try:
            return super().create(request, *args, **kwargs)
        except exceptions.TelegramIDAlreadyUsed as exc:
            raise ValidationError({"telegram_id": str(exc)}) from exc

    @extend_schema(
        request=serializers.ClientProfileUpsertSerializer,
        responses={200: serializers.ClientProfileUpsertSerializer},
        description="Create or update ClientProfile by telegram_id",
    )
    @action(detail=False, methods=["post"], url_path="upsert")
    def upsert(self, request) -> Response:
        serializer = serializers.ClientProfileUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_id = serializer.validated_data.pop("telegram_id")
        profile = self._get_profile_by_telegram_id(telegram_id)

        if profile:
            updated_profile = serializer.update(profile, serializer.validated_data)
            status_code = status.HTTP_200_OK
        else:
            updated_profile = serializer.create(
                {
                    **serializer.validated_data,
                    "telegram_id": telegram_id,
                }
            )
            status_code = status.HTTP_201_CREATED

        response_serializer = serializers.ClientProfileUpsertSerializer(updated_profile)
        return Response(response_serializer.data, status=status_code)

    @extend_schema(
        description="Restore a previously soft-deleted ClientProfile by ID.",
        responses={
            200: OpenApiResponse(description="Successfully restored."),
            400: OpenApiResponse(description="Already active."),
            404: OpenApiResponse(description="Not found."),
        },
    )
    @action(detail=True, methods=["get"])
    def restore(self, request, pk: int = None) -> Response:
        profile = self._get_profile_including_deleted(pk)

        if profile.deleted_at is None:
            return Response(
                {"detail": "Profile is already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile.restore()
        return Response({"detail": "Profile restored successfully."})

    def _get_profile_by_telegram_id(self, telegram_id: int) -> ClientProfile | None:
        return ClientProfile.objects.filter(
            telegram_ids__telegram_id=telegram_id
        ).first()

    def _get_profile_including_deleted(self, pk: int) -> ClientProfile:
        return get_object_or_404(ClientProfile.all_objects.filter(pk=pk))


@extend_schema(
    description="Get profile by Telegram ID in URL",
    responses={200: ClientProfileShortSerializer},
)
class ClientProfileByTelegramView(APIView):
    def get(self, request, telegram_id: int) -> Response:
        profile = get_object_or_404(
            ClientProfile.objects.filter(telegram_ids__telegram_id=telegram_id)
        )
        serializer = ClientProfileShortSerializer(profile)
        return Response(serializer.data)


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = serializers.GoalSerializer
