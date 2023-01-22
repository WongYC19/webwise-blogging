from rest_framework.permissions import BasePermission
from django.contrib.contenttypes.models import ContentType

class IsObjectAccessibleToUser(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.is_superuser:
                return True

            elif request.user.is_anonymous:
                return False

            content_type = request.data.get('content_type')
            object_id = request.data.get('object_id')

            try:
                content_type = ContentType.objects.get(model=content_type)
            except ContentType.DoesNotExist:
                return False
            else:
                obj = content_type.get_object_for_this_type(pk=object_id)
                if not obj.exists():
                    return False
            try:
                return bool(obj.is_published == True)
            except:
                return bool(obj.post.is_published == True)
        else:
            return True