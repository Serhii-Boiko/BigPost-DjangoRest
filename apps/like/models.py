from django.contrib.auth.models import User
from django.db import models
from generic_helpers.models import GenericRelationModel


class Like(GenericRelationModel):
    cancelled = models.BooleanField(
        verbose_name="cancelled",
        default=False
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
        verbose_name = "like"
        verbose_name_plural = "likes"
        ordering = ['-date_created']
        unique_together = ['content_type', 'object_pk', 'author']

    def __str__(self):
        return u"{}@{}".format(self.author, self.date_created)

    @staticmethod
    def like_object(content_object, user):
        try:
            existing_like = Like.objects.get(content_object=content_object, author=user)
            existing_like.cancelled = not existing_like.cancelled
            existing_like.save(force_update=True)
        except Like.DoesNotExist:
            Like(content_object=content_object, author=user).save()