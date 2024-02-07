from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    A personalized user manager where email is the unique identifier
    for authentication instead of the username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a user with the given email address and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = None
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """A custom user model to include UUID"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _('username'), max_length=150, unique=False, blank=True, null=True)

    email = models.EmailField(unique=True, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
