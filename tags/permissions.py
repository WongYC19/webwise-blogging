from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin to create, update or delete
    tagged items, but allow anyone to read them.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow anyone to read
        return request.user and request.user.is_staff  # Only admin can create, update or delete
