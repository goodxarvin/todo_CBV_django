from rest_framework import viewsets
from ...models import Objective
from .serializers import ObjectiveSerializer
from rest_framework.permissions import IsAuthenticated
from .paginations import ObjectivePagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


"""createing an api base on viewsets with drf"""

class ObjectiveViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated,]
    serializer_class = ObjectiveSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"status":["exact"]}
    search_fields = ["id", "title", "description",]
    ordering_fields = ["created_at", "updated_at"]
    pagination_class = ObjectivePagination

    def get_queryset(self):
        return Objective.objects.filter(owner=self.request.user)