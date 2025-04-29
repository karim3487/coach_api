from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema):
        """
        Override default schema for pagination in drf-spectacular.
        """
        return {
            "type": "object",
            "properties": {
                "total_items": {"type": "integer", "example": 42},
                "total_pages": {"type": "integer", "example": 5},
                "current_page": {"type": "integer", "example": 2},
                "next": {
                    "type": "string",
                    "format": "uri",
                    "nullable": True,
                    "example": "http://.../page=3",
                },
                "previous": {
                    "type": "string",
                    "format": "uri",
                    "nullable": True,
                    "example": "http://.../page=1",
                },
                "results": schema,
            },
        }
