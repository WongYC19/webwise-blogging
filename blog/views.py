from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from .models import Profile, Post, Comment
from .serializers import UserProfileSerializer, PostSerializer, CommentSerializer
from .permissions import IsAdminOrProfileOwner, CommentPermission

# Create your views here.
class UserProfileViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            # ? Only Admin allows to update/delete posts
            self.permission_classes = [IsAdminOrProfileOwner]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class PostViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user

        if not user.is_staff:
            return Post.objects.filter(is_published=True)

        return Post.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & CommentPermission]

    def get_queryset(self):
        print(self.kwargs)
        post_id = self.kwargs.get('post_pk')
        user = self.request.user

        if user.is_superuser:
            return Comment.objects.filter(post=post_id)

        return Comment.objects.select_related('post').filter(post_id=post_id, post__is_published=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.kwargs)
        return context

    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         # ? Only Admin or authenticated comment owner can update/delete comments
    #         return [IsAdminOrCommentOwner()]
    #     return [IsAuthenticated()]
