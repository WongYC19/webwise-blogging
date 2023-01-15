from rest_framework.permissions import BasePermission

class IsAdminOrCommentOwner(BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        return bool((obj.user == request.user) or (request.user.is_superuser == True))

class IsAdminOrProfileOwner(BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        return bool((obj.user == request.user) or (request.user.is_staff))