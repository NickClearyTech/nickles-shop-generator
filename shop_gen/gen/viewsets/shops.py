from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from gen.serializers import ShopSerializer, ShopSettingsSerializer
from gen.models import Shop, Job, ItemToShop
from gen.generator.generate_shop import generate_shop
from gen.tasks.generate_shop import generate_shop_task


class ShopViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Shop.objects.select_related("owner")
        return Shop.objects.filter(owner=self.request.user)

    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def create(self, request, **kwargs):
        serialized: ShopSettingsSerializer = ShopSettingsSerializer(
            data=request.data, context={"request": self.request}
        )
        serialized.is_valid(raise_exception=True)

        shop_object = generate_shop(serialized)

        return Response(
            status=status.HTTP_200_OK, data=ShopSerializer(shop_object).data
        )

    @action(
        detail=False, methods=["POST"], name="CreateShopAsync", url_path="create_async"
    )
    def create_async(self, request, **kwargs):
        serialized: ShopSettingsSerializer = ShopSettingsSerializer(
            data=request.data, context={"request": self.request}
        )
        serialized.is_valid(raise_exception=True)

        job_object: Job = Job()
        job_object.launched_by = self.request.user
        job_object.job_type = Job.JobType.GENERATE_SHOP
        job_object.job_parameters = serialized.data
        job_object.save()

        generate_shop_task.apply_async(args=[job_object.id])

        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_path=r"(?P<item_id>\d+)/(?P<quantity>\d+)",
        name="ShopItem",
    )
    def edit_item_quantity_in_shop(self, request, pk=None, item_id=None, quantity=None):
        try:
            shop = Shop.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                {"Not Found": "Shop not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            shop_to_item: ItemToShop = ItemToShop.objects.get(shop=pk, item=item_id)
        except ObjectDoesNotExist:
            return Response(
                {"Not Found": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        int_quant = int(quantity)

        if quantity is None or int_quant < 0:
            return Response({"Invalid": "Quantity must be greater than or equal to 0"})
        if int_quant == 0:
            shop_to_item.delete()
        else:
            shop_to_item.quantity = int_quant
            shop_to_item.save()

        return Response(ShopSerializer(instance=shop).data, status=status.HTTP_200_OK)
