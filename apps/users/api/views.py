from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer
from apps.users.services import register_user, login_user
from apps.users.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserInactiveError,
)


class RegisterAPIView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register_user(
                **serializer.validated_data
            )

        except UserAlreadyExistsError:
            return Response(
                {'detail': 'User already exists'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'id': user.id,
                'email': user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = login_user(
                request=request,
                **serializer.validated_data,
            )

        except InvalidCredentialsError:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except UserInactiveError:
            return Response(
                {'detail': 'User account is inactive'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                'access': result['access'],
                'refresh': result['refresh'],
            },
            status=status.HTTP_200_OK,
        )
