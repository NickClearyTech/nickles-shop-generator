from rest_framework import mixins
from rest_framework import permissions, viewsets

from gen.models import System
from gen.serializers import SystemSerializer


class SystemViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    queryset = System
    serializer_class = SystemSerializer
    permission_classes = [permissions.IsAuthenticated]
