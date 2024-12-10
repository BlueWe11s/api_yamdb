from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Genre, Review, Title

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import (IsAdminOnly, IsAdminorIsModerorIsSuperUser,
                             IsAdminOrReadOnly)
from api.serializers import (AuthSerializer, CategorySerializer,
                             CommentSerializer, GenreSerializer,
                             ListDetailedTitleSerializer, ReviewSerializer,
                             TitleSerializer, TokenSerializer, UserSerializer)

User = get_user_model()


class UserSignupView(APIView):
    '''
    Регистрация нового пользователя
    '''
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(
            username=request.data.get('username'),
            email=request.data.get('email')
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код - {confirmation_code}',
            settings.SENDER_EMAIL,
            [request.data.get('email')]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ObtainTokenView(TokenObtainPairView):
    '''
    Получение токена
    '''
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=request.data.get('username')
        )
        if not default_token_generator.check_token(
                user, request.data.get('confirmation_code')
        ):
            return Response(
                'Неверный confirmation_code',
                status=status.HTTP_400_BAD_REQUEST
            )
        token = {'token': str(AccessToken.for_user(user))}
        return Response(token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    '''
    Работа с пользователями
    '''
    serializer_class = UserSerializer
    queryset = User.objects.order_by('pk')
    permission_classes = (IsAdminOnly,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    pagination_class = PageNumberPagination
    http_method_names=['get', 'delete', 'post', 'patch']

    @action(
        methods=['GET', 'PATCH'], detail=False, url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_update_me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            if self.request.method == 'PATCH':
                serializer.validated_data.pop('role', None)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


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
    queryset = Title.objects.order_by('pk')
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
        if self.request.method == 'POST':
            if review:
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
