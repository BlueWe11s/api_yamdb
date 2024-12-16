from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Review, Title

from api.reviews.filters import TitleFilter
from api.reviews.mixins import ListCreateDestroyViewSet
from api.users.permissions import (
    IsAdminorIsModerorIsSuperUser,
    IsAdminOrReadOnly)
from api.reviews.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ListDetailedTitleSerializer,
    ReviewSerializer,
    TitleSerializer)


User = get_user_model()


class CategoryViewSet(ListCreateDestroyViewSet):
    '''
    Работа с категориями
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Работа с жанрами
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    '''
    Работа с произведениями
    '''
    http_method_names = ['get', 'delete', 'post', 'head', 'options', 'patch']
    queryset = Title.objects.order_by('pk').annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return ListDetailedTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    '''
    Работа с отзывами
    '''
    http_method_names = ['get', 'delete', 'post', 'head', 'options', 'patch']
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminorIsModerorIsSuperUser,)
    pagination_class = PageNumberPagination

    def object_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        title = self.object_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.object_title()
        review = Review.objects.filter(title=title, author=self.request.user)
        if review.exists():
            raise PermissionDenied(
                'Вы уже оставляли отзыва на это произведение.'
            )
        serializer.save(author=self.request.user, title=title)

    def get_serializer_context(self):
        return {'title_id': self.kwargs['title_id'], 'request': self.request}


class CommentViewSet(viewsets.ModelViewSet):
    '''
    Работа с комментариями
    '''
    http_method_names = ['get', 'delete', 'post', 'head', 'options', 'patch']
    serializer_class = CommentSerializer
    permission_classes = (IsAdminorIsModerorIsSuperUser,)
    pagination_class = PageNumberPagination

    def object_review(self):
        return get_object_or_404(
            Review.objects.filter(title_id=self.kwargs.get('title_id')),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        review = self.object_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.object_review()
        serializer.save(author=self.request.user, review=review)
