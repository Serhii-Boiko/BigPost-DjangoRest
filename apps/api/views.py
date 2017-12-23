from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.permissions import IsOwnerOrAdminOrReadOnly
from apps.like.models import Like
from apps.like.serializers import LikeSerializer

from apps.post.models import Post
from apps.comment.models import Comment
from apps.post.serializers import PostSerializer, BriefPostSerializer
from apps.comment.serializers import CommentSerializer, SubCommentSerializer


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200


class PostList(generics.ListCreateAPIView):
    """
    Posts list
    """

    ITEMS_PER_PAGE = 20

    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BriefPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        last_uuid = self.request.GET.get('last_uuid')
        queryset = Post.objects.all()

        if last_uuid:
            last_post = Post.objects.get(uuid=last_uuid)
            queryset = queryset.filter(id__lt=last_post.id)

        return queryset[:self.ITEMS_PER_PAGE]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Post details
    """
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly)
    serializer_class = PostSerializer
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.delete()


class PostCommentsList(generics.ListCreateAPIView):
    """
    Post's comments list
    """
    def get_queryset(self):
        post = get_object_or_404(Post, uuid=self.kwargs.get('post_uuid'))
        return Comment.objects.filter(content_object=post, parent=None)

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, uuid=self.kwargs.get('post_uuid'))
        serializer.save(
            author=self.request.user,
            content_object=post
        )


class PostSubCommentsList(generics.ListCreateAPIView):
    """ Post comment sub-comments list """
    def get_queryset(self):
        post = get_object_or_404(Post, uuid=self.kwargs.get('post_uuid'))
        comment = get_object_or_404(Comment, uuid=self.kwargs.get('comment_uuid'))
        return Comment.objects.filter(content_object=post, parent=comment)

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubCommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, uuid=self.kwargs.get('post_uuid'))
        comment = get_object_or_404(Comment, uuid=self.kwargs.get('comment_uuid'))
        serializer.save(
            author=self.request.user,
            content_object=post,
            parent=comment
        )


class PostLikesList(APIView):
    """
    Post's likes list
    """

    def _get_likes(self, post_uuid):
        post = get_object_or_404(Post, uuid=post_uuid)
        return Like.objects.filter(content_object=post, cancelled=False)

    def _get_response_dict(self, request, post_uuid):
        likes = self._get_likes(post_uuid)
        serializer = LikeSerializer(likes, many=True)
        return {
            "is_liked": request.user.id in likes.values_list('author', flat=True),
            "count": likes.count(),
            "results": serializer.data
        }

    def get(self, request, post_uuid):
        return Response(self._get_response_dict(request, post_uuid))

    def post(self, request, post_uuid):
        post = get_object_or_404(Post, uuid=post_uuid)
        like, created = Like.objects.get_or_create(content_object=post, author=request.user)
        like.date_created = timezone.now()
        like.cancelled = False
        like.save()
        return Response(self._get_response_dict(request, post_uuid),
                        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def delete(self, request, post_uuid):
        post = get_object_or_404(Post, uuid=post_uuid)
        like = get_object_or_404(Like, content_object=post, author=request.user)
        like.cancelled = True
        like.save()
        return Response(self._get_response_dict(request, post_uuid),
                        status=status.HTTP_200_OK)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Comment details
    """
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly)
    serializer_class = CommentSerializer
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.delete()


class CommentLikesList(APIView):
    """
    Comment's likes list
    """

    def _get_likes(self, comment_uuid):
        comment = get_object_or_404(Comment, uuid=comment_uuid)
        return Like.objects.filter(content_object=comment, cancelled=False)

    def _get_response_dict(self, request, comment_uuid):
        likes = self._get_likes(comment_uuid)
        serializer = LikeSerializer(likes, many=True)
        return {
            "is_liked": request.user.id in likes.values_list('author', flat=True),
            "count": likes.count(),
            "results": serializer.data
        }

    def get(self, request, post_uuid, comment_uuid):
        return Response(self._get_response_dict(request, comment_uuid))

    def post(self, request, post_uuid, comment_uuid):
        comment = get_object_or_404(Comment, uuid=comment_uuid)
        like, created = Like.objects.get_or_create(content_object=comment, author=request.user)
        like.date_created = timezone.now()
        like.cancelled = False
        like.save()
        return Response(self._get_response_dict(request, comment_uuid),
                        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def delete(self, request, post_uuid, comment_uuid):
        comment = get_object_or_404(Comment, uuid=comment_uuid)
        like = get_object_or_404(Like, content_object=comment, author=request.user)
        like.cancelled = True
        like.save()
        return Response(self._get_response_dict(request, comment_uuid),
                        status=status.HTTP_200_OK)