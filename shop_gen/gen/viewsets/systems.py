from rest_framework import mixins
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from gen.models import System
from gen.serializers import SystemSerializer


class SystemViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
