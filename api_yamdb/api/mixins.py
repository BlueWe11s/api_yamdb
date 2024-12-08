from rest_framework import filters, mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    '''
    Представление для работы с моделями
    '''
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
