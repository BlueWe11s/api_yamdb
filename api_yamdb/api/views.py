from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Users
from api.permissions import IsAdminOnly, IsAdminorIsModerorIsSuperUser, IsAdminOrReadOnly
from reviews.models import Category, Genre, Review, Title

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
        serializer = 
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
    serializer_class = 
    premission = ('IsAdminOnly',)

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,))
    def AuthUser(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = 
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = 
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    

class ObtainTokenView(APIView):
    """Класс для запроса на получение токена."""
    def post(self, request):
        serializer = 
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.get_token_for_user(user)
        return Response(token, status=status.HTTP_200_OK)
