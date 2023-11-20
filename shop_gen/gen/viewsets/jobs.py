from rest_framework import mixins, permissions, viewsets

from gen.serializers import JobSerializer
from gen.models import Job


class JobViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Job.objects.all()
        return Job.objects.filter(launched_by=self.request.user)

    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
