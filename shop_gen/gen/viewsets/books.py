from rest_framework import mixins
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from gen.models import Book
from gen.serializers import BookSerializer


class BookViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ["system", "abbreviation"]
    search_fields = ["system", "system__name", "full_name", "abbreviation"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
