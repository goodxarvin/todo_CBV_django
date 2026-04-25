from rest_framework import viewsets
from ...models import Objective
from .serializers import ObjectiveSerializer
from rest_framework.permissions import IsAuthenticated


"""createing an aip nase on viewsets with drf"""


class ObjectiveViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = ObjectiveSerializer
    def get_queryset(self):
        return Objective.objects.filter(owner=self.request.user)