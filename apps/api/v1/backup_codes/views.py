from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.backup_codes import serializers
from apps.profiles import exceptions
from apps.profiles.models import ClientProfile
from apps.profiles.services.backup_code_service import BackupCodeService


@extend_schema(
    request=serializers.GenerateCodesInputSerializer,
    responses={
        200: OpenApiResponse(
            response=list[str], description="List of generated backup codes"
        ),
        404: OpenApiResponse(description="Client with given Telegram ID not found"),
    },
    examples=[
        OpenApiExample(
            name="Generate Codes",
            value={"telegram_id": 123456789, "count": 5},
            request_only=True,
        ),
        OpenApiExample(
            name="Response",
            value=["code1abc", "code2def", "code3ghi"],
            response_only=True,
        ),
    ],
    description="Generate backup codes for the user by Telegram ID",
)
class GenerateBackupCodesView(APIView):
    def post(self, request):
        serializer = serializers.GenerateCodesInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id = serializer.validated_data["telegram_id"]

        service = BackupCodeService()
        try:
            codes = service.generate_by_tg_id(
                telegram_id=telegram_id,
                count=serializer.validated_data["count"],
            )
        except ClientProfile.DoesNotExist:
            return Response(
                {"detail": f"Client with Telegram ID = {telegram_id} does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(codes)


@extend_schema(
    request=serializers.UseCodeInputSerializer,
    responses={
        200: OpenApiResponse(
            response=dict, description="Telegram ID successfully linked"
        ),
        400: OpenApiResponse(
            description="Backup code is invalid, used, or Telegram ID already linked"
        ),
    },
    examples=[
        OpenApiExample(
            name="Use Backup Code",
            value={"code": "X9K7-P8F1", "telegram_id": 987654321},
            request_only=True,
        ),
        OpenApiExample(
            name="Success Response",
            value={"detail": "Telegram ID linked to profile 12"},
            response_only=True,
        ),
        OpenApiExample(
            name="Invalid Code",
            value={"detail": "Backup code is invalid or already used"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
    description="Use backup code to link a Telegram ID to an existing ClientProfile",
)
class UseBackupCodeView(APIView):
    def post(self, request):
        serializer = serializers.UseCodeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = BackupCodeService()
        try:
            profile = service.link_telegram_id(
                code=serializer.validated_data["code"],
                telegram_id=serializer.validated_data["telegram_id"],
            )
        except exceptions.BackupCodeInvalidOrAlreadyUsed:
            return Response(
                {"detail": "Backup code is invalid or already used"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except exceptions.TelegramIDAlreadyLinked:
            return Response(
                {"detail": "Telegram ID is already linked to another profile"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": f"Telegram ID linked to profile {profile.id}"})
