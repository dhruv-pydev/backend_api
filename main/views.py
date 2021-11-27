from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, viewsets
from main.models import BaseUser

from main.serializers import BaseUserSerializer


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
    queryset = BaseUser.objects.select_related("user").all()
