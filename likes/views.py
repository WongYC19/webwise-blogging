from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin

from .models import Like
from .serializers import LikeSerializer
from .permissions import IsObjectAccessibleToUser

User = get_user_model()

# Create your views here.
class LikeViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            detail = e.detail['detail']
            error = detail['error']
            status_code = int(detail.get('status_code', 400))
            return Response(error, status=status_code)

        user = request.user
        data = serializer.validated_data
        content_type = data['content_type']
        object_id = data['object_id']

        like, created = Like.objects.get_or_create(user_id=user.pk, content_type=content_type, object_id=object_id)

        # Unlike to the existing post/comment
        if not created:
            like.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        like.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)