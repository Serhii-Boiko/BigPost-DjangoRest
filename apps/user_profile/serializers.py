from rest_framework import serializers

from apps.user_profile.models import UserProfile


class UserProfileBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('uuid', 'full_name', 'absolute_url')

    def get_full_name(self, obj):
        return u"{} {}".format(obj.first_name, obj.last_name)
    full_name = serializers.SerializerMethodField(read_only=True)

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    absolute_url = serializers.SerializerMethodField(read_only=True)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('uuid', 'first_name', 'last_name', 'email', 'about', 'absolute_url')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    absolute_url = serializers.SerializerMethodField(read_only=True)