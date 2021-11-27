from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import BaseUserViewSet, LoginView

router = DefaultRouter()

router.register("user", BaseUserViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
