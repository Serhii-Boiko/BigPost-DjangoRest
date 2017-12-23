from rest_framework import serializers

from apps.comment.models import Comment
from apps.like.models import Like
from apps.like.serializers import LikeSerializer
from apps.user_profile.serializers import UserProfileBriefSerializer


class SubCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('uuid', 'text', 'parent_uuid', 'date_created', 'author',
                  'likes_count', 'likes', 'is_liked')

    def get_parent_uuid(self, obj):
        return obj.parent.uuid if obj.parent else None
    parent_uuid = serializers.SerializerMethodField(read_only=True)

    author = UserProfileBriefSerializer(read_only=True, source='author.profile')

    likes = LikeSerializer(read_only=True, many=True, source='get_last_likes')

    def get_likes_count(self, obj):
        return Like.objects.filter(content_object=obj, cancelled=False).count()
    likes_count = serializers.SerializerMethodField(read_only=True)

    def get_is_liked(self, obj):
        likes = Like.objects.filter(content_object=obj, cancelled=False)
        return self.context['request'].user.id in likes.values_list('author', flat=True)
    is_liked = serializers.SerializerMethodField(read_only=True)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('uuid', 'text', 'date_created', 'author', 'replies',
                  'likes_count', 'likes', 'is_liked')

    replies = SubCommentSerializer(read_only=True, many=True)

    author = UserProfileBriefSerializer(read_only=True, source='author.profile')

    likes = LikeSerializer(read_only=True, many=True, source='get_last_likes')

    def get_likes_count(self, obj):
        return Like.objects.filter(content_object=obj, cancelled=False).count()
    likes_count = serializers.SerializerMethodField(read_only=True)

    def get_is_liked(self, obj):
        likes = Like.objects.filter(content_object=obj, cancelled=False)
        return self.context['request'].user.id in likes.values_list('author', flat=True)
    is_liked = serializers.SerializerMethodField(read_only=True)