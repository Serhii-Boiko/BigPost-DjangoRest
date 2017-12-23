from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models

from apps.abstract.model import AbstractUUID
from apps.comment.models import Comment
from apps.like.models import Like


class Post(AbstractUUID):
    title = models.CharField(
        verbose_name="title",
        max_length=250, null=True, blank=True
    )
    text = models.TextField(
        verbose_name="text",
        validators=[MaxLengthValidator(2000)]
    )
    date_created = models.DateTimeField(
        verbose_name="date created",
        auto_now_add=True,
    )
    author = models.ForeignKey(
        verbose_name="author",
        to=User
    )

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def get_comments_count(self):
        return Comment.objects.filter(content_object=self).count()

    def get_comments(self):
        return Comment.objects.filter(content_object=self)

    def get_last_comments(self):
        return Comment.objects.filter(content_object=self).order_by('date_created')[:3]

    def get_likes_count(self):
        return Like.objects.filter(content_object=self).count()

    def get_last_likes(self):
        return Like.objects.filter(content_object=self).order_by('date_created')[:3]

    def is_liked_by_user(self, user):
        return user.id in Like.objects.filter(content_object=self).values_list('author', flat=True)
