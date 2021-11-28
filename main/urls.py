from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import BaseUserViewSet, LoginView, QuestionViewSet, TagViewSet, AnswerViewSet

router = DefaultRouter()

router.register("user", BaseUserViewSet, basename="user")
router.register("tag", TagViewSet, basename="tag")
router.register("question", QuestionViewSet, basename="question")
router.register("answer", AnswerViewSet, basename="answer")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
