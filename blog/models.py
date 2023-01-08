from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

User = get_user_model()

# Create your models here.
class Post(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200, null=False)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} modified by {self.author}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} commented on '{self.post.title}'"