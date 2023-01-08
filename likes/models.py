from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class LikeManager(models.Manager):
    def likes_for_object(self, content_type, object_id):
        content_type = ContentType.objects.get_for_model(content_type)
        return self.filter(content_type=content_type, object_id=object_id)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeManager()