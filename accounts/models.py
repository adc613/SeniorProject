from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

import random


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name='Jane', last_name='Doe'):
        if not email:
            raise ValueError('User must have email')

        if not password:
            raise ValueError('User must have password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            )

        # Should be False but will leave it as True for now, because I don't
        # want to do email verification
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name="John",
                         last_name="Doe"):
        user = self.create_user(email, password, first_name, last_name)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    email = models.EmailField(unique=True)
    echo = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = False

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name


def passcode_init():
    return random.randrange(1000, 9999)


class LinkAccountToEcho(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    passcode = models.IntegerField(default=passcode_init)
    user = models.OneToOneField(User)
    active = models.BooleanField(default=True)
