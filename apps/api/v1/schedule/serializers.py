from rest_framework import serializers

from apps.api.v1.workouts.serializers import WorkoutSerializer
from apps.plans.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    workout_name = serializers.CharField(source="workout.name")

    class Meta:
        model = Schedule
        fields = (
            "id",
            "plan",
            "date",
            "time",
            "workout",
            "workout_name",
            "day_number",
            "completed",
            "completed_at",
            "notes",
        )
        read_only_fields = ("completed_at",)


class ScheduleDetailSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = (
            "id",
            "plan",
            "date",
            "time",
            "workout",
            "day_number",
            "completed",
            "completed_at",
            "notes",
        )
        read_only_fields = ("completed_at",)


class ScheduleCompleteInputSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
