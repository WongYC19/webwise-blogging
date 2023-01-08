from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class TagManager(models.Manager):

    def get_tags_for(self, content_type, object_id):
        return self.filter(content_type=content_type, object_id=object_id)
class Tag(models.Model):
    label = models.CharField(max_length=200)
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()