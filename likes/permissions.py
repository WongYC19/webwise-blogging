from rest_framework.permissions import BasePermission
from django.contrib.contenttypes.models import ContentType

class IsAdminOrLikeObjectOwner(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                data = request.data
                content_type = ContentType.objects.get(pk=data['content_type'])
                liked_object = content_type.get_object_for_this_type(pk=data['object_id'])

                if request.user.is_staff or liked_object.user == request.user:
                    return True
            except:
                pass
        return False