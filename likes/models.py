from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class LikeManager(models.Manager):
    def get_likes_count(self, content_type, object_id):
        content_type = ContentType.objects.get_for_model(content_type)
        queryset = Like.objects.filter(content_type=content_type, object_id=object_id)
        return queryset.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey()

    objects = LikeManager()
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]