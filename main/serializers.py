from rest_framework import serializers
from .models import Answer, BaseUser, Question, Tag, Vote
from django.contrib.auth.models import User
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class BaseUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = BaseUser
        exclude = ["user", ]
        read_only_fields = ["id", ]

    def create(self, validated_data):
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        username = validated_data.pop("username", None)
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)

        user_dict = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
        }

        user = User.objects.create(**user_dict)
        user.set_password(password)
        user.save()

        validated_data["user"] = user

        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["id", ]


class QuestionSerializer(serializers.ModelSerializer):
    question_tags = serializers.ListField(required=False)
    related_tags = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    upvotes = serializers.IntegerField(read_only=True)
    downvotes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        exclude = ["user", "tags"]

    def get_related_tags(self, obj: Question):
        tags = obj.tags.all()
        return TagSerializer(tags, many=True).data

    def get_answers(self, obj: Question):
        answers = obj.question_answers.all()
        return AnswerSerializer(answers, many=True).data

    def validate(self, attrs):
        tags = attrs.pop("question_tags", None)
        all_tags = self.context.get("all_tags")
        tag_list = list()
        non_existing_tags = [tag for tag in list(
            tags) if not all_tags.filter(title=tag["title"]).exists()]

        if non_existing_tags:
            raise serializers.ValidationError({
                "question_tags": f"{non_existing_tags} does not exists!"
            })
        else:
            for tag in list(tags):
                tag_list.append(all_tags.get(title=tag["title"]))

            attrs["tags"] = tag_list

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        tags = validated_data.pop("tags", None)
        user = self.context.get("request").user
        base_user = user.base_user
        validated_data["user"] = base_user
        question = super(QuestionSerializer, self).create(validated_data)

        if tags:
            tags = [tag.id for tag in tags]
            question.tags.set(tags)

        return question


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(
        slug_field="id", queryset=Question.objects.all(), required=True)
    answered_by = serializers.CharField(read_only=True)

    class Meta:
        model = Answer
        exclude = ["user", ]

    def create(self, validated_data):
        user = self.context.get("request").user
        base_user = user.base_user
        validated_data["user"] = base_user
        return super().create(validated_data)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        exclude = ["user", ]

    def create(self, validated_data):
        user = self.context.get("request").user
        base_user = user.base_user
        validated_data["user"] = base_user
        return super().create(validated_data)
