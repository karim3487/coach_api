from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
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
        try:
            goal = Goal.objects.get(slug=slug)
        except Goal.DoesNotExist:
            return Response(
                {"detail": "Goal not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(GoalSerializer(goal).data)
