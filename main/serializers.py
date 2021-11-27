from rest_framework import serializers
from .models import BaseUser
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")


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
