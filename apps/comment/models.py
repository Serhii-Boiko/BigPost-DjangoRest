from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models

from generic_helpers.models import GenericRelationModel
from apps.abstract.model import AbstractUUID
from apps.like.models import Like


class Comment(AbstractUUID, GenericRelationModel):
    text = models.TextField(
        verbose_name="text",
        validators=[MaxLengthValidator(1000)]
    )
    parent = models.ForeignKey(
        verbose_name="parent comment",
        to='Comment', null=True, blank=True, related_name='replies'
    )
    date_created = models.DateTimeField(
        verbose_name="date created",
        auto_now_add=True
    )
    author = models.ForeignKey(
        verbose_name="author",
        to=User
    )

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ['date_created']

    def __str__(self):
        return self.text

    def get_last_likes(self):
        return Like.objects.filter(content_object=self).order_by('date_created')[:3]
