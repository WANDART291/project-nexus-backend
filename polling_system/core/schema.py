# core/schema.py
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            enum=[choice[0] for choice in Project.CATEGORY_CHOICES],
        )
    ]
)
class ProjectViewSet(viewsets.ModelViewSet):
    ...