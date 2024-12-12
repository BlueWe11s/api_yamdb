from rest_framework import filters, mixins, viewsets
from api_yamdb.api.users.permissions import (IsAdminOrReadOnly)
from rest_framework.pagination import PageNumberPagination


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Наследуемый класс
    """
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
