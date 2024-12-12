from api.users.views import ObtainTokenView, UserSignupView, UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'users'


users_router = DefaultRouter()
users_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', ObtainTokenView.as_view(), name='token'),
    path('v1/auth/signup/', UserSignupView.as_view()),
    path('v1/', include(users_router.urls)),
]
