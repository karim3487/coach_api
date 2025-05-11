from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.plans import schemas, serializers
from apps.plans import models
from apps.plans.choices import PlanStatus
from apps.plans.exceptions import ActivePlanExists, NoWorkoutsInProgram
from apps.plans.models import Plan
from apps.plans.services.plans import PlanService
from apps.plans.tasks import create_ai_plan_task
from apps.profiles.models import ClientProfile
from apps.programs.models import Program

# =========================================
# Read
# =========================================


@schemas.plan_list_schema
class PlanListView(generics.ListAPIView):
    queryset = models.Plan.objects.all()
    serializer_class = serializers.PlanSerializer


@schemas.plan_retrieve_schema
class PlanRetrieveView(generics.RetrieveAPIView):
    queryset = models.Plan.objects.all()
    serializer_class = serializers.PlanSerializer


@extend_schema(
    description="Get the current active plan by user's Telegram ID.",
    responses={
        200: serializers.PlanSerializer,
        404: OpenApiResponse(description="No active plan found."),
    },
)
@schemas.current_plan_by_telegram_schema
class CurrentPlanByTelegramView(APIView):
    def get(self, request, telegram_id: int):
        profile = get_object_or_404(
            ClientProfile, telegram_ids__telegram_id=telegram_id
        )
        plan = Plan.objects.filter(
            client_profile=profile, status=PlanStatus.ACTIVE
        ).first()

        if not plan:
            return Response(
                {"detail": "No active plan found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)


# =========================================
# Create AI Plan
# =========================================


class BaseCreatePlanView(APIView):
    """Base class for creating plans with ActivePlanExists handling."""

    def _create_plan_with_handling(self, creator_func, *args, **kwargs):
        try:
            plan = creator_func(*args, **kwargs)
            return Response(
                serializers.PlanSerializer(plan).data, status=status.HTTP_201_CREATED
            )
        except ActivePlanExists as ex:
            raise ValidationError(
                {"detail": "User already has an active training plan."}
            ) from ex
        except NoWorkoutsInProgram as ex:
            raise ValidationError(
                {"detail": "Program has no workouts to assign."}
            ) from ex


@schemas.create_ai_plan_by_profile_schema
class CreateAIPlanByProfileView(BaseCreatePlanView):
    def post(self, request):
        serializer = serializers.PlanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = get_object_or_404(
            ClientProfile, id=serializer.validated_data["profile_id"]
        )
        task = create_ai_plan_task.delay(profile.id)
        return Response(
            {"detail": "Plan creation started.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED,
        )


@schemas.create_ai_plan_by_telegram_schema
class CreateAIPlanByTelegramView(BaseCreatePlanView):
    def post(self, request):
        serializer = serializers.CreateAIPlanByTelegramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = get_object_or_404(
            ClientProfile,
            telegram_ids__telegram_id=serializer.validated_data["telegram_id"],
        )

        if Plan.objects.filter(
            client_profile=profile, status=PlanStatus.ACTIVE
        ).exists():
            raise ValidationError(
                {"detail": "User already has an active training plan."}
            )

        task = create_ai_plan_task.delay(profile.id)
        return Response(
            {"detail": "Plan creation started.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED,
        )


# =========================================
# Create Plan from Program
# =========================================


@schemas.create_plan_from_program_by_profile_schema
class CreatePlanFromProgramByProfileView(BaseCreatePlanView):
    def post(self, request):
        serializer = serializers.PlanCreateFromProgramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = get_object_or_404(
            ClientProfile, id=serializer.validated_data["profile_id"]
        )

        if Plan.objects.filter(
            client_profile=profile, status=PlanStatus.ACTIVE
        ).exists():
            raise ValidationError(
                {"detail": "User already has an active training plan."}
            )

        program = get_object_or_404(Program, id=serializer.validated_data["program_id"])

        return self._create_plan_with_handling(
            PlanService.create_training_plan, client=profile, program=program
        )


@schemas.create_plan_from_program_by_telegram_schema
class CreatePlanFromProgramByTelegramView(BaseCreatePlanView):
    def post(self, request):
        serializer = serializers.PlanCreateFromProgramByTelegramSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        profile = get_object_or_404(
            ClientProfile,
            telegram_ids__telegram_id=serializer.validated_data["telegram_id"],
        )
        program = get_object_or_404(Program, id=serializer.validated_data["program_id"])

        return self._create_plan_with_handling(
            PlanService.create_training_plan, client=profile, program=program
        )
