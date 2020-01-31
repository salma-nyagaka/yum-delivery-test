"""
configure common methods for testing
"""
from typing import Callable
from typing import Tuple
from typing import Type

import pytest

from leavemanagementsystem.apps.authentication.backends import \
    JWTAuthentication
from leavemanagementsystem.apps.authentication.models import User
from leavemanagementsystem.apps.role.models import Role


@pytest.fixture
def create_role(db):
    """
    create a db user
    """
    user_details = {
        "id": "-LgpYbY-puCzlUnY6sR0",
        "title": "Regular User",
        "description": "Leave Management System Regular User",
    }
    user1 = Role.objects.create(**user_details)
    user1.is_active = True  # activate user account
    user1.save()
    return user1


@pytest.fixture
def create_db_user(create_role, django_user_model: Type[User]) -> User:
    """
    create a db user
    """
    create_role
    user_details = {
        "username": "user1",
        "password": "pass123",
        "email": "user1@quexl.com",
    }
    user1 = django_user_model.objects.create_user(**user_details)
    user1.is_active = True  # activate user account
    user1.save()
    return user1


@pytest.fixture
def generate_access_token1(create_db_user: User) -> Tuple[str, User]:
    """
    """
    user1 = create_db_user
    user_details = {"username": user1.username, "email": user1.email}
    jwt = JWTAuthentication()
    encoded_token = jwt.generate_token(user_details)
    return encoded_token, user1


@pytest.fixture
def generate_access_token2(create_db_user2: User) -> Tuple[str, User]:
    """
    """
    user2 = create_db_user2
    user_details = {"username": user2.username, "email": user2.email}
    jwt = JWTAuthentication()
    encoded_token = jwt.generate_token(user_details)
    return encoded_token, user2


@pytest.fixture
def create_superuser(django_user_model: Type[User]) -> User:
    superuser_details = {
        "username": "superuser1",
        "password": "passSuper3",
        "email": "super@quexl.com",
    }
    superuser = django_user_model.objects.create_superuser(**superuser_details)
    superuser.is_active = True
    superuser.save()
    return superuser


@pytest.fixture()
def generate_superuser_access_token(create_superuser: User) -> str:
    """
    generate superuser token
    """
    superuser = create_superuser
    details = {"username": superuser.username, "email": superuser.email}
    jwt = JWTAuthentication()
    encoded_token = jwt.generate_token(details)
    return encoded_token


@pytest.fixture
def create_db_user2(django_user_model: Type[User]) -> User:
    """
    create a db user
    """
    user_details = {
        "username": "user2",
        "password": "pass123",
        "email": "user2@quexl.com"
    }
    user2 = django_user_model.objects.create_user(**user_details)
    user2.is_active = True  # activate user account
    user2.save()
    return user2


@pytest.fixture()
def generate_new_token(django_user_model: Type[User]) -> Callable:
    """
    generate new jwt tokn for givn user credentials
    """

    def _generate_new_token(**kwargs):
        username = kwargs.get("username")
        details = {
            "username": username,
            "password": kwargs.get("password", "pass1234"),
            "email": f"{username}@quexl.com",
        }
        user = django_user_model.objects.create(**details)
        user.is_active = True  # activate user
        user.save()
        details.pop("password")  # remove password from jwt payload
        jwt = JWTAuthentication()
        token = jwt.generate_token(details)

        return token, user

    return _generate_new_token
