from rest_framework import serializers


class GenerateCodesInputSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    count = serializers.IntegerField(default=10, min_value=1, max_value=20)


class UseCodeInputSerializer(serializers.Serializer):
    code = serializers.CharField()
    telegram_id = serializers.IntegerField()
