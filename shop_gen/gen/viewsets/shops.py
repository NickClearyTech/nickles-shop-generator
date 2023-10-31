from rest_framework.response import Response
from rest_framework import mixins, permissions, viewsets, status

from gen.serializers import ShopSerializer, ShopSettingsSerializer
from gen.models import Shop, Job
from gen.tasks.generate_shop import generate_shop


class ShopViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Shop.objects.all()
        return Shop.objects.filter(owner=self.request.user)

    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serialized: ShopSettingsSerializer = ShopSettingsSerializer(
            data=request.data, context={"request": self.request}
        )
        serialized.is_valid(raise_exception=True)
        job_object: Job = Job()
        job_object.launched_by = self.request.user
        job_object.job_type = Job.JobType.GENERATE_SHOP
        job_object.job_parameters = serialized.data
        job_object.save()

        generate_shop.apply_async(args=[job_object.id])

        return Response({"ok": "okay"}, status=status.HTTP_200_OK)
