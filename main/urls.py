from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import BaseUserViewSet, LoginView, QuestionViewSet, TagViewSet

router = DefaultRouter()

router.register("user", BaseUserViewSet, basename="user")
router.register("tag", TagViewSet, basename="tag")
router.register("question", QuestionViewSet, basename="question")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
