from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    title = models.CharField(max_length=200, null=False)
    slug = models.SlugField(unique=True, editable=False)
    content = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} modified by {self.author}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.user} commented on '{self.post.title}'"

    class Meta:
        ordering =['-modified_date']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    github_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.email})"