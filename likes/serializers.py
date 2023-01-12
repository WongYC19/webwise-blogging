from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import Like

class LikeSerializer(serializers.ModelSerializer):

    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model',
    )

    class Meta:
        model = Like
        fields = ['content_type', 'object_id', 'user']
        read_only_fields = ('user', )

    def validate(self, data):
        print(f"Data: {data}")
        content_type = data['content_type']
        accepted_models = ['post', 'comment']
        accepted_values = ", ".join(map(lambda  x: "`" + x + "`", accepted_models))

        # Validate the given content type is accepted models
        if content_type.model not in accepted_models:
            raise serializers.ValidationError(f"The provided content type `{content_type}` is not available. Accepts {accepted_values} only")

        content_type = ContentType.objects.get_for_model(model=content_type)

        # Validate the existence of the target object (Post/Comment instance)
        object_id = data['object_id']
        Model = data['content_type'].model_class()

        if not Model.objects.filter(pk=object_id).exists():
            raise serializers.ValidationError(f"The provided object id `{object_id}` is not found in `{Model.__name__}` model.")

        data['object_id'] = object_id
        return data
