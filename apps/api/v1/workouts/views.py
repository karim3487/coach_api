from rest_framework import viewsets

from apps.api.v1.workouts import serializers
from apps.workouts.models import Workout, WorkoutExercise


class WorkoutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Workout.objects.prefetch_related("workoutexercise_set__exercise").all()
    serializer_class = serializers.WorkoutSerializer


class WorkoutExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = serializers.WorkoutExerciseSerializer
