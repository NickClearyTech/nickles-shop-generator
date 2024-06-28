from rest_framework import mixins, permissions, viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from gen.serializers import SpellSerializer
from gen.querysets.item_queries import get_spells


class SpellViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    def get_queryset(self):
        return get_spells(self.request.user)

    serializer_class = SpellSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
