import logging

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.db.models import Q
from django.utils.translation import pgettext_lazy

from leavemanagementsystem.apps.role.models import Role
from leavemanagementsystem.helpers.fancy_generator import fancy_id_generator

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_staff=False,
                    **extra_fields):
        """Create a user instance with the given email and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        if email is None:
            raise TypeError('Users must have an email address.')

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)

        if password:
            user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.save()

        return user

    def regular_user(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & Q(trips__isnull=False))
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(db_index=True,
                          max_length=256,
                          default=fancy_id_generator,
                          primary_key=True,
                          editable=False)

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    role = models.ForeignKey(Role,
                             on_delete=models.CASCADE,
                             default='-LgpYbY-puCzlUnY6sR0')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the username field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    class Meta:
        permissions = (
            ("manage_users",
             pgettext_lazy("Permission description", "Manage regular users."),
             ),
            ("manage_staff",
             pgettext_lazy("Permission description", "Manage staff."),
             ),
            ("impersonate_users",
             pgettext_lazy("Permission description", "Impersonate users."),
             ),
        )

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    @staticmethod
    def get_user(email):
        try:
            user = User.objects.get(email=email)
            return user

        except Exception:
            return False

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.objects.get(id=user_id)
            return user

        except Exception:
            return False
