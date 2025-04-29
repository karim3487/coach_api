from rest_framework import serializers

from apps.api.v1.exercises.serializers import ExerciseShortSerializer
from apps.exercises.models import Exercise
from apps.workouts.models import Workout, WorkoutExercise


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        source="exercise",
        write_only=True,
    )

    class Meta:
        model = WorkoutExercise
        fields = [
            "id",
            "exercise_id",
            "sets",
            "reps",
            "duration",
            "rest_interval",
            "order",
            "notes",
        ]
        read_only_fields = ["id"]


class WorkoutExerciseReadSerializer(serializers.ModelSerializer):
    exercise = ExerciseShortSerializer()

    class Meta:
        model = WorkoutExercise
        fields = [
            "id",
            "exercise",
            "sets",
            "reps",
            "duration",
            "rest_interval",
            "order",
            "notes",
        ]


class WorkoutExerciseCreateSerializer(serializers.ModelSerializer):
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        source="exercise",
        write_only=True,
    )

    class Meta:
        model = WorkoutExercise
        fields = [
            "exercise_id",
            "sets",
            "reps",
            "duration",
            "rest_interval",
            "order",
            "notes",
        ]


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseCreateSerializer(many=True, write_only=True)
    exercises_list = WorkoutExerciseReadSerializer(
        source="workoutexercise_set", many=True, read_only=True
    )

    class Meta:
        model = Workout
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "description",
            "duration_est",
            "goal",
            "level",
            "active",
            "exercises",
            "exercises_list",
        ]
        read_only_fields = ["id", "slug"]

    def create(self, validated_data):
        exercises_data = validated_data.pop("exercises", [])
        workout = Workout.objects.create(**validated_data)
        WorkoutExercise.objects.bulk_create(
            [
                WorkoutExercise(workout=workout, **exercise_data)
                for exercise_data in exercises_data
            ]
        )
        return workout

    def update(self, instance, validated_data):
        exercises_data = validated_data.pop("exercises", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if exercises_data is not None:
            instance.workoutexercise_set.all().delete()
            WorkoutExercise.objects.bulk_create(
                [
                    WorkoutExercise(workout=instance, **exercise_data)
                    for exercise_data in exercises_data
                ]
            )

        return instance


class SimpleWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["id", "name", "duration_est"]
