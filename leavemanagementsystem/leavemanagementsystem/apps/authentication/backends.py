"""Configure JWT Here"""

import datetime
import logging

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

"""Configure JWT Here"""

# Get an instance of a logger
logger = logging.getLogger(__name__)


class JWTAuthentication(TokenAuthentication):
    """Inherit the JSON web authentication class from rest_framework_jwt"""
    keyword = 'Bearer'

    @staticmethod
    def generate_token(userdata):
        """
        method to generate a payload token
        """
        secret = settings.SECRET_KEY
        token = jwt.encode({
            'userdata': userdata,
            'iat': datetime.datetime.utcnow(),
            'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, secret)
        # decode the byte type token
        token = token.decode('utf-8')
        return token

    @staticmethod
    def decode_jwt(token):
        """ Method for decoding token."""
        # It takes the token, secret_key and algorithm
        user_details = jwt.decode(token, settings.SECRET_KEY,
                                  algorithm='HS256')
        return user_details

    def authenticate_credentials(self, key):
        try:
            # decode the payload and get the user
            payload = jwt.decode(key, settings.SECRET_KEY)
            user = get_user_model().objects.get(username=payload['userdata']['username'])   # noqa E501
        except (jwt.DecodeError, get_user_model().DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        return user, payload
