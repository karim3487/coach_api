from rest_framework import serializers

from apps.api.v1.goals.serializers import GoalSerializer
from apps.profiles import exceptions, models


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


class ClientProfileShortSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)
    goal = serializers.SerializerMethodField()

    class Meta:
        model = models.ClientProfile
        exclude = (
            "id",
            # "contraindications",
            "created_at",
            "updated_at",
            "deleted_at",
        )

    def get_goal(self, obj):
        return obj.goal.name if obj.goal else None


class ClientProfileCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.ClientProfile
        exclude = ("id", "created_at", "updated_at", "deleted_at")

    def create(self, validated_data):
        telegram_id = validated_data.pop("telegram_id")
        exists = models.ClientProfile.objects.filter(
            telegram_ids__telegram_id=telegram_id
        ).exists()
        if exists:
            raise exceptions.TelegramIDAlreadyUsed()
        profile = models.ClientProfile.objects.create(**validated_data)
        models.TelegramID.objects.create(telegram_id=telegram_id, profile=profile)
        return profile


class ClientProfileUpsertSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)
    goal = serializers.PrimaryKeyRelatedField(
        queryset=models.Goal.objects.all(), write_only=True
    )
    goal_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ClientProfile
        exclude = ("created_at", "updated_at", "deleted_at")

    def create(self, validated_data):
        telegram_id = validated_data.pop("telegram_id")
        profile = models.ClientProfile.objects.create(**validated_data)
        models.TelegramID.objects.create(profile=profile, telegram_id=telegram_id)
        return profile

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_goal_display(self, obj):
        return obj.goal.name if obj.goal else None
