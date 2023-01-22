from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework import status

from .models import Like
class CustomValidationError(serializers.ValidationError):
    def __init__(self, *args, **kwargs):
        kwargs['status_code'] = 404
        super().__init__(*args, **kwargs)
class LikeSerializer(serializers.ModelSerializer):

    content_type = serializers.CharField(max_length=255)

    class Meta:
        model = Like
        fields = ['content_type', 'object_id', 'user']
        read_only_fields = ('user', )

    def validate(self, data):

        content_type = data['content_type']
        object_id = data['object_id']

        accepted_models = ['post', 'comment']
        accepted_values = ", ".join(map(lambda  x: "`" + x + "`", accepted_models))

        user = self.context['request'].user
        # Return 401 if user is not authenticated
        if user.is_anonymous:
            raise serializers.ValidationError({ "detail": {
                "error": f"User is not authenticated. Please login.",
                "status_code": 401
            }})

        if content_type not in accepted_models:
            raise serializers.ValidationError({ "detail": {
                "error": f"The provided content type `{content_type}` is not available. Accepts {accepted_values} only",
                "status_code": 400
            }})

        content_type = ContentType.objects.get(model=content_type)

        data['object_id'] = object_id
        data['content_type'] = content_type

        # Validate the existence of the target object (Post/Comment instance)
        Model = content_type.model_class()

        if user.is_superuser:
            return data

        objects = Model.objects.filter(pk=object_id)

        if not objects.exists():
            raise serializers.ValidationError({ "detail": {
                "error": f"The selected `{content_type}` not found.",
                "status_code": 404
            }})

        object = objects.first()

        try:
            if not object.is_published:
                raise serializers.ValidationError({"detail": {
                    "error": "You have no right to like/dislike the private post.",
                    "status_code": 403,
                }})
        except AttributeError:
            if not object.post.is_published:
                raise serializers.ValidationError({"detail": {
                    "error": "You have no right to like/dislike the comments under private post.",
                    "status_code": 403,
            }})

        return data
