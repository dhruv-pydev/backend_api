from django.http.response import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status, viewsets
from lib.renderer import CustomJSONRenderer

from main.models import Answer, BaseUser, Question, Tag
from main.serializers import AnswerSerializer, BaseUserSerializer, QuestionSerializer, TagSerializer, VoteSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.base_user and user.base_user.is_active is False:
            raise ValidationError(
                {"non_field_errors": [f"User is not active."]}
            )
        token, created = Token.objects.get_or_create(user=user)
        print(dir(token))
        data = {"token": token.key}
        return Response(data=data, status=status.HTTP_200_OK)


class BaseUserViewSet(viewsets.ModelViewSet):
    serializer_class = BaseUserSerializer
    renderer_classes = [CustomJSONRenderer]
    queryset = BaseUser.objects.prefetch_related(
        "user_questions", "user_answers", "user_votes").select_related("user").all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    renderer_classes = [CustomJSONRenderer]
    queryset = Tag.objects.prefetch_related("question_tags").all()


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    renderer_classes = [CustomJSONRenderer]
    queryset = Question.objects.prefetch_related(
        "tags", "question_answers", "question_votes").select_related("user").all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        context["all_tags"] = Tag.objects.all()
        return context

    @action(methods=["GET", "POST"], detail=True, renderer_classes=[CustomJSONRenderer])
    def answer(self, request, *args, **kwargs):
        question_id = kwargs.get("pk", None)
        if request.method == "GET":
            answers = Answer.objects.filter(question__id=question_id)
            data = AnswerSerializer(answers, many=True).data
            return JsonResponse({
                "data": data,
                "message": "Data retrieved successfully!"
            }, status=status.HTTP_200_OK)
        else:
            request_data = request.data
            request_data.update({"question": question_id})
            answer_serializer = AnswerSerializer(
                data=request_data, context={"request": request})
            if answer_serializer.is_valid():
                answer_serializer.save()
                return JsonResponse({
                    "data": QuestionSerializer(self.get_object()).data,
                    "message": "Data retrieved successfully!"
                }, status=status.HTTP_200_OK)
            else:
                raise serializers.ValidationError(answer_serializer.errors)

    @action(methods=["POST", "GET"], detail=True, renderer_classes=[CustomJSONRenderer])
    def vote(self, request, *args, **kwargs):
        question_id = kwargs.get("pk", None)
        if request.method == "GET":
            pass
        else:
            request_data = request.data
            request_data.update({"question": question_id})
            vote_serializer = VoteSerializer(
                data=request_data, context={"request": request})
            if vote_serializer.is_valid():
                vote_serializer.save()
                return JsonResponse({
                    "data": "",
                    "message": "Vote added successfully!"
                })
            else:
                raise serializers.ValidationError(vote_serializer.errors)
        # VoteSerializer


# class AnswerViewSet(viewsets.ModelViewSet):
#     serializer_class = AnswerSerializer
#     renderer_classes = [CustomJSONRenderer]
#     queryset = Answer.objects.prefetch_related(
#         "answer_votes").select_related("user", "question").all()

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request
#         return context
