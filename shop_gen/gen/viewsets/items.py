from rest_framework import mixins, permissions, viewsets

from gen.serializers import ItemSerializer
from gen.querysets import get_items


class ItemViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    def get_queryset(self):
        return get_items(self.request.user)

    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
