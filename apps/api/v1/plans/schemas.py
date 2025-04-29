from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from apps.api.v1.plans import serializers

# -------------- Read ---------------- #

plan_list_schema = extend_schema(responses={200: serializers.PlanSerializer(many=True)})

plan_retrieve_schema = extend_schema(responses={200: serializers.PlanSerializer})

current_plan_by_telegram_schema = extend_schema(
    description="Get the current active plan by user's Telegram ID.",
    responses={
        200: serializers.PlanSerializer,
        404: OpenApiResponse(description="No active plan found."),
    },
)

# -------------- Create AI ------------- #

create_ai_plan_by_profile_schema = extend_schema(
    request=serializers.PlanCreateSerializer,
    responses={
        201: serializers.PlanSerializer,
        400: OpenApiResponse(description="Invalid input"),
        404: OpenApiResponse(description="Profile not found"),
    },
    examples=[
        OpenApiExample(
            name="Create AI Plan", value={"profile_id": 1}, request_only=True
        )
    ],
)

create_ai_plan_by_telegram_schema = extend_schema(
    request=serializers.CreateAIPlanByTelegramSerializer,
    responses={
        201: serializers.PlanSerializer,
        400: OpenApiResponse(description="Invalid input"),
        404: OpenApiResponse(description="Profile not found"),
    },
)

# -------------- Create from Program ------------- #

create_plan_from_program_by_profile_schema = extend_schema(
    request=serializers.PlanCreateFromProgramSerializer,
    responses={
        201: serializers.PlanSerializer,
        400: OpenApiResponse(description="Invalid input"),
        404: OpenApiResponse(description="Profile not found / Program not found"),
    },
    examples=[
        OpenApiExample(
            name="Create Plan From Program",
            value={"profile_id": 1, "program_id": 2},
            request_only=True,
        )
    ],
)

create_plan_from_program_by_telegram_schema = extend_schema(
    request=serializers.PlanCreateFromProgramByTelegramSerializer,
    responses={
        201: serializers.PlanSerializer,
        400: OpenApiResponse(description="Invalid input"),
        404: OpenApiResponse(description="Profile not found / Program not found"),
    },
    examples=[
        OpenApiExample(
            name="Create Plan From Program by Telegram",
            value={"telegram_id": 123456789, "program_id": 2},
            request_only=True,
        )
    ],
)
