from django.urls import include, path
from rest_framework import routers

from .views import UserRegistrationView


urlpatterns = [
    path('v1/signup/', UserRegistrationView.as_view(), name='signup'),
]
