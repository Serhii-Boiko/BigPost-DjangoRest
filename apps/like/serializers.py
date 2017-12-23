from rest_framework import serializers

from apps.like.models import Like
from apps.user_profile.serializers import UserProfileBriefSerializer


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('author', 'date_created')

    author = UserProfileBriefSerializer(read_only=True, source='author.profile')
