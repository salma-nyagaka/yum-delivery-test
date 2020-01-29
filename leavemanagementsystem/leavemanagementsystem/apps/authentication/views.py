import os
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from leavemanagementsystem.apps.authentication.backends import \
    JWTAuthentication
from leavemanagementsystem.apps.authentication.email import send_email
from leavemanagementsystem.helpers.endpoint_response import \
    get_success_responses
from .models import User
from .renderers import UserJSONRenderer
from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationAPIView(GenericAPIView):
    """Register a new user"""
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request, **kwargs):
        """ Signup a new user """
        email, username, password = request.data.get(
            'email', None), request.data.get(
            'username', None), request.data.get('password', None)

        user = {"email": email, "username": username, "password": password}

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        send_email(request, user)

        serializer.save()

        response_data = {
            "username": username,
            "email": email
        }

        return get_success_responses(
            data=response_data,
            message="Please confirm your account by clicking on the "
                    "link sent to your email account {}".format(email),
            status_code=status.HTTP_201_CREATED
        )

    def get(self, request):
        return Response(
            data={
                "message": 'Only POST requests are allowed to this endpoint.'
            })


class UserActivationAPIView(GenericAPIView):
    """Activate a user after mail verification."""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def get(self, request, token, *args, **kwargs):
        """ Method for getting user token and activating them. """
        # After a successful registration, a user is activated through here
        # The token that was created and sent is decoded to get the user
        # The user's is_active attribute is then set to true
        try:
            data = JWTAuthentication.decode_jwt(token)
            user = User.objects.get(username=data['userdata'])
        except:
            return Response(
                data={"message": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return redirect('http://127.0.0.1:8000/api/users/verified')


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """Login a user"""
        email, password = request.data.get('email', None), request.data.get(
            'password', None)

        user = {"email": email, "password": password}
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data

        user = User.get_user(user_data['email'])
        userdata = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "image": user.photo,
            "role_id": user.role_id,
        }
        user_data['token'] = \
            JWTAuthentication.generate_token(userdata=userdata)

        return get_success_responses(
            data=user_data,
            message="You have successfully logged in",
            status_code=status.HTTP_200_OK
        )

    def get(self):
        """Get a user"""
        return Response(
            data={
                "message": 'Only post requests are allowed to this endpoint.'
            })
