from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.goals.serializers import GoalSerializer
from apps.profiles.models import Goal


class GoalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


@extend_schema(
    description="Get Goal by slug",
    responses={200: GoalSerializer, 404: {"detail": "Not found"}},
)
class GoalBySlugView(APIView):
    def get(self, request, slug):
        goal = get_object_or_404(Goal, slug=slug)
        return Response(GoalSerializer(goal).data)
