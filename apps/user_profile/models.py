from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models

from apps.abstract.model import AbstractUUID


class UserProfile(AbstractUUID):
    user = models.OneToOneField(
        verbose_name="user",
        to=User, related_name="profile"
    )
    first_name = models.CharField(
        verbose_name="first name",
        max_length=50
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=50
    )
    email = models.EmailField(
        verbose_name="email",
        max_length=150, null=True, blank=True
    )
    about = models.TextField(
        verbose_name="about",
        validators=[MaxLengthValidator(2000)], null=True, blank=True
    )

    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "users profiles"
        ordering = ['pk']

    def __str__(self):
        return u"{} {}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return '/profile/{0}/'.format(self.uuid)
