from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import viewsets

from apps.api.v1.profiles import serializers
from apps.profiles.models import ClientProfile


class ClientProfileViewSet(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = serializers.ClientProfileSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.ClientProfileCreateSerializer
        super().get_serializer_class()

    @extend_schema(
        request=serializers.ClientProfileCreateSerializer,
        responses={201: serializers.ClientProfileSerializer},
        examples=[
            OpenApiExample(
                name="Create ClientProfile Example",
                value={
                    "name": "Ali",
                    "age": 30,
                    "weight": 75.5,
                    "height": 180.0,
                    "gender": "male",
                    "training_location": "gym",
                    "available_days": ["mon", "wed", "fri"],
                    "preferred_time": "18:00:00",
                    "goal": 1,
                    "telegram_id": 123456789,
                },
                request_only=True,
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
