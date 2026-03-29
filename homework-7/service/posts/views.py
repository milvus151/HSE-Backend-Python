from pickle import FALSE

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Post, Comment, PostLike, CommentLike
from .serializers import PostReadSerializer, PostCreateSerializer, CommentSerializer, UserSerializer, PostLikeSerializer, CommentLikeSerializer
from .permissions import IsAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema, no_body

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={200: "Краткий список пользователей (только логины)"})
    @action(detail=False, methods=['get'])
    def names_only(self, request):
        users = User.objects.values('id', 'username')
        return Response(users)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PostReadSerializer
        return PostCreateSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(post=post, author=request.user)
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

    @swagger_auto_schema(responses={200: "Легковесный список постов (только ID и заголовки)"})
    @action(detail=False, methods=['get'])
    def lightweight(self, request):
        posts = Post.objects.values_list('id', 'title')
        return Response(posts)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        post_id = serializer.validated_data.get('post_id')
        if not post_id:
            post_id = self.request.data.get('post_id')

        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        comment = self.get_object()
        like, created = CommentLike.objects.get_or_create(comment=comment, author=request.user)
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

class PostLikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

class CommentLikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer