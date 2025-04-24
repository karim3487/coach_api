from rest_framework import serializers

from apps.profiles import models


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = ["id", "name", "slug", "description"]


class TelegramIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TelegramID
        fields = ["telegram_id"]


class ClientProfileSerializer(serializers.ModelSerializer):
    goal = GoalSerializer(read_only=True)
    telegram_ids = TelegramIDSerializer(many=True, read_only=True)

    class Meta:
        model = models.ClientProfile
        fields = "__all__"


class ClientProfileCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.ClientProfile
        exclude = ("created_at", "updated_at", "deleted_at")

    def create(self, validated_data):
        telegram_id = validated_data.pop("telegram_id")
        profile = models.ClientProfile.objects.create(**validated_data)
        models.TelegramID.objects.create(telegram_id=telegram_id, profile=profile)
        return profile
