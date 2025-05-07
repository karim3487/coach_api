from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.plans.models import Progress
from apps.profiles.models import ClientProfile


class ProgressSerializer(serializers.ModelSerializer):
    workout_name = serializers.CharField(source="workout.name", read_only=True)
    exercise_name = serializers.CharField(source="exercise.name", read_only=True)

    class Meta:
        model = Progress
        fields = (
            "id",
            "client_profile",
            "date",
            "plan",
            "workout",
            "workout_name",
            "exercise",
            "exercise_name",
            "metric",
            "value",
            "units",
            "notes",
        )


class ProgressCreateByTelegramSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Progress
        exclude = ("client_profile", "created_at", "updated_at", "deleted_at")

    def create(self, validated_data):
        telegram_id = validated_data.pop("telegram_id")
        profile = get_object_or_404(
            ClientProfile, telegram_ids__telegram_id=telegram_id
        )
        return Progress.objects.create(client_profile=profile, **validated_data)
