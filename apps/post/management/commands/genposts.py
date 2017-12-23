from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from apps.post.models import Post


class Command(BaseCommand):

    def handle(self, *args, **options):
        count = int(args[0]) if len(args) else 1
        user = User.objects.all().order_by('?')[0]

        for i in range(count):
            post = Post(text="Text", author=user)
            post.save()
            post.title = u"Post #{0}".format(post.id)
            post.text = u"Text for {0}.".format(post.uuid)
            post.save()
