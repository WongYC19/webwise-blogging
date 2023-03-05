from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Tag, TaggedItem

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["pk", "label"]

class TaggedItemSerializer(serializers.ModelSerializer):
    label = serializers.CharField(write_only=True)
    tags = TagSerializer(read_only=True, many=True)
    content_type = serializers.CharField(max_length=255)

    class Meta:
        model = TaggedItem
        fields = ["id", "label", "content_type", "object_id", "created_date", "modified_date", "tags"]

    def validate(self, data):
        content_type_str = data['content_type']
        content_type = get_object_or_404(ContentType, model=content_type_str)

        data['content_type'] = content_type
        return data

    @transaction.atomic
    def save(self):
        """ Add tag to targeted type of instance """
        validated_data = self.validated_data
        tag_label = validated_data['label']
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']
        # tagged_item = validated_data['tagged_item']

        tag, _ = Tag.objects.get_or_create(label=tag_label)
        tagged_item = TaggedItem.objects.filter(content_type=content_type, object_id=object_id).first()

        if tagged_item is None:
            raise serializers.ValidationError("The specified tagged item does not exist.", code=404)

        if tag in tagged_item.tags.all():
            tagged_item.tags.remove(tag)
        else:
            tagged_item.tags.add(tag)

        tagged_item.save()

        return tagged_item