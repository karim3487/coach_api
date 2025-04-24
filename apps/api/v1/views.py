from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


@extend_schema(responses={"200": {"type": "string"}})
@api_view()
def hello_world(request):
    return Response({"message": "Hello World!"})


@api_view(["GET"])
def api_root(request):
    return Response({"message": "Welcome to API v1"})
