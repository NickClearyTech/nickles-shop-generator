from rest_framework import mixins, permissions, viewsets

from gen.serializers import SpellSerializer
from gen.querysets import get_spells


class SpellViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    def get_queryset(self):
        return get_spells(self.request)

    serializer_class = SpellSerializer
    permission_classes = [permissions.IsAuthenticated]
