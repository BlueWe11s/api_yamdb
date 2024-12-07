from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, ObtainTokenView, UserSignupView

app_name = 'users'

users_router = DefaultRouter()
users_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', ObtainTokenView, name='token'),
    path('v1/auth/signup/', UserSignupView),
    path('v1/', include(users_router.urls)),
]
