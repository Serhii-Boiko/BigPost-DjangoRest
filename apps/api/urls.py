from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from apps.api import views


urlpatterns = format_suffix_patterns([
    url(r'^posts/$', views.PostList.as_view(), name='api_posts_list'),
    url(r'^posts/(?P<uuid>[a-f0-9]{32})/$', views.PostDetail.as_view(), name='api_post_detail'),
    url(r'^posts/(?P<post_uuid>[a-f0-9]{32})/likes/$', views.PostLikesList.as_view(), name='api_post_likes'),
    url(r'^posts/(?P<post_uuid>[a-f0-9]{32})/comments/$', views.PostCommentsList.as_view(),
        name='api_post_comments_list'),
    url(r'^posts/(?P<post_uuid>[a-f0-9]{32})/comments/(?P<comment_uuid>[a-f0-9]{32})/$',
        views.PostSubCommentsList.as_view(), name='api_post_subcomments_list'),
    url(r'^posts/(?P<post_uuid>[a-f0-9]{32})/comments/(?P<comment_uuid>[a-f0-9]{32})/likes/$',
        views.CommentLikesList.as_view(), name='api_comment_likes'),
    url(r'^comments/(?P<comment_uuid>[a-f0-9]{32})/$', views.CommentDetail.as_view(), name='api_comment_detail'),
])

urlpatterns += [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
