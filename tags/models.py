from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
class TagManager(models.Manager):

    def get_tags_for(self, object_type, object_id):
        content_type = ContentType.objects.get_for_model(object_type)

        return self.prefetch_related('tag').filter(content_type=content_type, object_id=object_id).first()
class Tag(models.Model):
    """ This model represents a single tag with a label/name. It holds the metadata for the tag."""
    label = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.label} ({self.pk})"
class TaggedItem(models.Model):
    """
        This model represents a relationship between a tag and some other objects in the system.
        Defining these moddels separately to have more flexibility reuse tag across different types of objects.
        Helps to query more efficiently for all objects associated to a particular tag without performing full-text search over all object records.
    """
    tags = models.ManyToManyField(Tag, related_name='tagged_items')
    # tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagged_items')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = TagManager()

    def __str__(self):
        return f"Type: {self.content_type}, Object ID: {self.object_id}, Tag: {self.tag}"

    # def save(self, *args, **kwargs) -> None:
    #     print(self)
    #     if not self.tag:
    #         self.tag, _ = Tag.objects.get_or_create(name='placeholder')
    #     self.save(*args, **kwargs)

class DummyModel(models.Model):
    name = models.CharField(max_length=255)
        # created_date = models.DateTimeField(auto_now_add=True)
        # modified_date = models.DateTimeField(auto_now=True)
        # tags = models.ManyToManyField(TaggedItem)
        # tags = GenericRelation(TaggedItem)

        # class Meta:
            # db_table = "DummyModel"
