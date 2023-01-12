from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Create your views here.
class PostViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Post.objects.all()

        return Post.objects.filter(is_published=True)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        comments = Comment.objects.filter(post_id=post_id)
        return comments

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.kwargs)
        return context