from rest_framework import mixins, permissions, viewsets

from gen.serializers import ShopSerializer
from gen.models import Shop


class ShopViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Shop.objects.all()
        return Shop.objects.filter(owner=self.request.user)

    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]