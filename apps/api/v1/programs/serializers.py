from rest_framework import serializers

from apps.api.v1.workouts.serializers import SimpleWorkoutSerializer
from apps.programs import models


class ProgramSerializer(serializers.ModelSerializer):
    goal = serializers.StringRelatedField()

    class Meta:
        model = models.Program
        fields = [
            "id",
            "name",
            "slug",
            "goal",
            "description",
            "days_per_week",
            "duration_weeks",
            "level",
            "location_type",
            "active",
        ]


class ProgramDetailSerializer(serializers.ModelSerializer):
    goal = serializers.StringRelatedField()
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = models.Program
        fields = [
            "id",
            "name",
            "slug",
            "goal",
            "description",
            "days_per_week",
            "duration_weeks",
            "level",
            "location_type",
            "active",
            "schedule",
        ]


class ProgramWorkoutSerializer(serializers.ModelSerializer):
    workout = SimpleWorkoutSerializer()

    class Meta:
        model = models.ProgramWorkout
        fields = ["week_number", "day_number", "workout"]
