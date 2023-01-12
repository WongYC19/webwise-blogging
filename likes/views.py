from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import LikeSerializer
from .models import Like

User = get_user_model()

# Create your views here.
class LikeViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def create(self, request, *args, **kwargs):
        # user = request.user
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        content_type = data['content_type']
        object_id = data['object_id']
        user = User(pk=1)
        like, created = Like.objects.get_or_create(user=user, content_type=content_type, object_id=object_id)

        # Unlike to the existing post/comment
        if not created:
            like.delete()
            return Response(request.data, status=status.HTTP_204_NO_CONTENT)

        like.save()
        return Response(request.data, status=status.HTTP_201_CREATED)