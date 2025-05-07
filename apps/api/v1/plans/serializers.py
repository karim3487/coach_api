from rest_framework import serializers

from apps.api.v1.schedule.serializers import ScheduleSerializer
from apps.plans.models import Plan
from apps.profiles.models import ClientProfile
from apps.programs.models import Program


class PlanSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(many=True, source="schedule_set", read_only=True)
    goal_name = serializers.SerializerMethodField()
    program_name = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = (
            "id",
            "client_profile",
            "program",
            "program_name",
            "goal",
            "goal_name",
            "start_date",
            "end_date",
            "status",
            "progress_percent",
            "schedule",
        )

    def get_goal_name(self, obj: Plan) -> str:
        return obj.goal.name if obj.goal else ""

    def get_program_name(self, obj: Plan) -> str:
        return obj.program.name if obj.program else ""


class PlanCreateSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()

    def validate_profile_id(self, value):
        if not ClientProfile.objects.filter(id=value).exists():
            raise serializers.ValidationError("Client profile not found.")
        return value


class PlanCreateFromProgramByTelegramSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    program_id = serializers.IntegerField()

    def validate(self, attrs):
        telegram_id = attrs.get("telegram_id")
        program_id = attrs.get("program_id")

        if not ClientProfile.objects.filter(
            telegram_ids__telegram_id=telegram_id
        ).exists():
            raise serializers.ValidationError(
                {"telegram_id": "ClientProfile not found."}
            )

        if not Program.objects.filter(id=program_id, active=True).exists():
            raise serializers.ValidationError(
                {"program_id": "Program not found or inactive."}
            )

        return attrs


class PlanCreateFromProgramSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    program_id = serializers.IntegerField()

    def validate(self, attrs):
        profile_id = attrs.get("profile_id")
        program_id = attrs.get("program_id")

        if not ClientProfile.objects.filter(id=profile_id).exists():
            raise serializers.ValidationError(
                {"profile_id": "ClientProfile not found."}
            )

        if not Program.objects.filter(id=program_id, active=True).exists():
            raise serializers.ValidationError(
                {"program_id": "Program not found or inactive."}
            )

        return attrs


class CreateAIPlanByTelegramSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()

    def validate_telegram_id(self, value):
        from apps.profiles.models import TelegramID

        if not TelegramID.objects.filter(telegram_id=value).exists():
            raise serializers.ValidationError("Telegram ID not found.")
        return value
