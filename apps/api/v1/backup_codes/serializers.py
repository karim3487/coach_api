from rest_framework import serializers

from apps.profiles.models import ClientProfile


class GenerateCodesInputSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    count = serializers.IntegerField(default=10, min_value=1, max_value=20)

    def validate(self, attrs):
        telegram_id = attrs.get("telegram_id")

        if not ClientProfile.objects.filter(
            telegram_ids__telegram_id=telegram_id
        ).exists():
            raise serializers.ValidationError(
                {"profile_id": "ClientProfile with provided telegram_id not found."}
            )

        return attrs


class UseCodeInputSerializer(serializers.Serializer):
    code = serializers.CharField()
    telegram_id = serializers.IntegerField()
