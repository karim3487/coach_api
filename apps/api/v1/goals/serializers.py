from rest_framework import serializers

from apps.profiles import models


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = ["id", "name", "slug", "description"]
