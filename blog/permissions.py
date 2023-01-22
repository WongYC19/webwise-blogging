from rest_framework.permissions import BasePermission
from .models import Post
from django.shortcuts import get_object_or_404

class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        post_id = view.kwargs['post_pk']
        post = get_object_or_404(Post, id=post_id)
        if (post.is_published) or (request.user.is_superuser):
            return True
        else:
            return False
    ...
    def has_object_permission(self, request, view, obj) -> bool:
        # Check if the post is public or superuser
        if (obj.post.is_published) or (request.user.is_superuser):
            return True

        return False

class IsAdminOrProfileOwner(BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        return bool((obj.user == request.user) or (request.user.is_staff))