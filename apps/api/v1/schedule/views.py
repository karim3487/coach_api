import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.schedule import serializers
from apps.api.v1.workouts.serializers import WorkoutSerializer
from apps.plans.models import Schedule
from apps.profiles.models import ClientProfile
from apps.workouts.models import Workout


@extend_schema(responses=serializers.ScheduleSerializer(many=True))
class ScheduleListView(generics.ListAPIView):
    queryset = Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer


@extend_schema(responses=serializers.ScheduleSerializer)
class ScheduleRetrieveView(generics.RetrieveAPIView):
    queryset = Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer


@extend_schema(
    request=serializers.ScheduleCompleteInputSerializer,
    responses={
        200: OpenApiResponse(
            description="Successful confirmation message.",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name="Workout Completed",
                    value={"detail": "Workout marked as complete."},
                    response_only=True,
                )
            ],
        ),
        404: OpenApiResponse(
            description="Not found",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name="Profile Not Found",
                    value={"detail": "No ClientProfile matches the given query."},
                    response_only=True,
                ),
                OpenApiExample(
                    name="Schedule Not Found",
                    value={"detail": "No Schedule matches the given query."},
                    response_only=True,
                ),
            ],
        ),
    },
)
class ScheduleCompleteView(APIView):
    def post(self, request):
        serializer = serializers.ScheduleCompleteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_id = serializer.validated_data["telegram_id"]

        profile = get_object_or_404(
            ClientProfile, telegram_ids__telegram_id=telegram_id
        )

        schedule = get_object_or_404(
            Schedule.objects.filter(
                date=datetime.date.today(),
                plan__client_profile=profile,
            )
        )

        schedule.completed = True
        schedule.completed_at = schedule.completed_at or timezone.now()
        schedule.save()

        return Response(
            {"detail": "Workout marked as complete."}, status=status.HTTP_200_OK
        )


class GetTodayWorkoutView(APIView):
    def get(self, request, telegram_id):
        profile = get_object_or_404(
            ClientProfile, telegram_ids__telegram_id=telegram_id
        )
        workout = get_object_or_404(
            Workout.objects.filter(
                schedule__date=datetime.date.today(),
                schedule__plan__client_profile=profile,
            )
        )
        return Response(WorkoutSerializer(workout).data)


@extend_schema(
    summary="Get today's workout schedule by Telegram ID",
    description="Returns today's Schedule entry for the given Telegram user ID.",
    responses={
        200: serializers.ScheduleDetailSerializer,
        404: OpenApiResponse(description="Schedule or user not found"),
    },
    parameters=[
        OpenApiParameter(
            name="telegram_id",
            description="Telegram user ID",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
)
class GetTodayScheduleView(APIView):
    def get(self, request, telegram_id):
        profile = get_object_or_404(
            ClientProfile, telegram_ids__telegram_id=telegram_id
        )
        schedule = get_object_or_404(
            Schedule.objects.filter(
                date=datetime.date.today(), plan__client_profile=profile
            )
        )
        return Response(serializers.ScheduleDetailSerializer(schedule).data)


@extend_schema(
    summary="List all schedule entries by telegram_id",
    description="Returns all scheduled workouts for a user by Telegram ID.",
    parameters=[
        OpenApiParameter(
            name="telegram_id",
            required=True,
            type=int,
            location=OpenApiParameter.QUERY,
            description="Telegram ID of the user",
        ),
    ],
    responses=serializers.ScheduleSerializer(many=True),
)
class ScheduleListByTelegramView(generics.ListAPIView):
    serializer_class = serializers.ScheduleSerializer

    def get_queryset(self):
        telegram_id = self.request.query_params.get("telegram_id")
        profile = get_object_or_404(
            ClientProfile, telegram_ids__telegram_id=telegram_id
        )
        return Schedule.objects.filter(plan__client_profile=profile).order_by(
            "date", "time"
        )
