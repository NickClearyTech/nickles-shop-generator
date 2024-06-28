from django.contrib.auth.models import User
from rest_framework import mixins, status
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from gen.serializers import UserSerializer, UserSelfSerializer

from gen.serializers import ShopToItemSerializer

from gen.models import Shop, ItemToShop


class UserViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    def get_queryset(self):
        if self.action == "get_me":
            return User.objects.get(self.request.user)
        return User.objects.all().order_by("-date_joined")

    def get_serializer_class(self):
        if self.action == "get_me":
            return UserSelfSerializer
        return UserSerializer

    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="Get Self",
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_me(self, request):
        shop = Shop.objects.first()
        queryset = ItemToShop.objects.filter(shop=shop)
        serializer = ShopToItemSerializer(instance=queryset, many=True)
        serializer.data

        serialized: UserSelfSerializer = UserSelfSerializer(instance=request.user)
        return Response(serialized.data, status=status.HTTP_200_OK)
