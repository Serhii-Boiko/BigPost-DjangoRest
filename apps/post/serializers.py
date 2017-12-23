from rest_framework import serializers

from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer
from apps.like.models import Like
from apps.like.serializers import LikeSerializer
from apps.post.models import Post
from apps.user_profile.serializers import UserProfileBriefSerializer


class BriefPostSerializer(serializers.ModelSerializer):
    """ Post serializer """
    class Meta:
        model = Post
        fields = ('uuid', 'title', 'text', 'date_created', 'author',
                  'comments_count', 'likes_count')

    author = UserProfileBriefSerializer(read_only=True, source='author.profile')

    def get_likes_count(self, obj):
        return Like.objects.filter(content_object=obj, cancelled=False).count()
    likes_count = serializers.SerializerMethodField(read_only=True)

    def get_comments_count(self, obj):
        print(Comment.objects.get_for_object(obj))
        return Comment.objects.get_for_object(obj).count()
    comments_count = serializers.SerializerMethodField(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    """ Post serializer """
    class Meta:
        model = Post
        fields = ('uuid', 'title', 'text', 'date_created', 'author',
                  'comments_count', 'comments',
                  'likes_count', 'likes', 'is_liked')

    author = UserProfileBriefSerializer(read_only=True, source='author.profile')

    comments = CommentSerializer(read_only=True, many=True, source='get_last_comments')
    likes = LikeSerializer(read_only=True, many=True, source='get_last_likes')

    def get_likes_count(self, obj):
        return Like.objects.filter(content_object=obj, cancelled=False).count()
    likes_count = serializers.SerializerMethodField(read_only=True)

    def get_comments_count(self, obj):
        print(Comment.objects.get_for_object(obj))
        return Comment.objects.get_for_object(obj).count()
    comments_count = serializers.SerializerMethodField(read_only=True)

    def get_is_liked(self, obj):
        likes = Like.objects.filter(content_object=obj, cancelled=False)
        return self.context['request'].user.id in likes.values_list('author', flat=True)
    is_liked = serializers.SerializerMethodField(read_only=True)