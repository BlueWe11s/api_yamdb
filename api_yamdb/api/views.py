from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from reviews.models import Category, Genre, Review, Title
from api.filters import TitleFilter
from api.permissions import (IsAdminOnly,
                          IsAdminorIsModerorIsSuperUser)
from api.serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer,
    UsersSerializer,
    AuthUsersSerializer,
    ObtainTokenSerializer,
    SignupSerializer
)
from api.mixins import ListCreateDestroyViewSet

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Users

User = get_user_model()


class UserSignupView(APIView):
    """
    Класс обработки запроса на получение кода.
    Если пользователя нет, то он будет создан и ему
    на email будет он выслан
    Если же он есть, то код пересоздается и также
    отправляется код на почту
    """
    def post(self, request):
        serializer = SignupSerializer
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = {
            'email': user.email,
            'username': user.username
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Класс обработки запросов с пользователями"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    premission = ('IsAdminOnly',)

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,))
    def AuthUser(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = AuthUsersSerializer
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = AuthUsersSerializer
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    

class ObtainTokenView(APIView):
    """Класс для запроса на получение токена."""
    def post(self, request):
        serializer = ObtainTokenSerializer
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.get_token_for_user(user)
        return Response(token, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOnly]


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOnly]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminorIsModerorIsSuperUser)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminorIsModerorIsSuperUser)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
