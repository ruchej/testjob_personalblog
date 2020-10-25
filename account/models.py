from django.db import models
from django.contrib.auth.hashers import make_password, identify_hasher
from django.contrib.auth.models import AbstractUser, UserManager


class AccountManager(UserManager):
    def get_managers(self):
        return super().get_managers().filter(is_staff=True)


class Account(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    objects = AccountManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        try:
            _alg = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)