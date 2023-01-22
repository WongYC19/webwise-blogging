from django.apps import apps
from django.contrib.auth import get_user_model

import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType

from django.urls import reverse

fake = Faker()
app = apps.get_app_config('blog')

User = get_user_model()
Post = app.get_model('Post')
Comment = app.get_model('Comment')

Like = apps.get_model("likes", "Like")

@pytest.fixture
def users():
    normal_user = User.objects.create_user(email=fake.email(), password=fake.password())
    superuser = User.objects.create_superuser(email=fake.email(), password=fake.password())
    anonymous_user = None
    return {
        "superuser": superuser,
        "normal_user": normal_user,
        "anonymous_user": anonymous_user,
    }

@pytest.fixture
def objects(users):
    # admin = baker.make(User, is_superuser=True, is_staff=True)
    # user = baker.make(User, is_superuser=False, is_staff=False)

    admin = users['superuser']
    user = users['normal_user']
    no_user = users['anonymous_user']

    post = baker.make(Post, author=admin, content=fake.text(), is_published=True)
    private_post = baker.make(Post, author=admin, content=fake.text(), is_published=False)

    comment = baker.make(Comment, post=post, user=admin, content=fake.text())
    comment_2 = baker.make(Comment, post=post, user=user, content=fake.text())

    comment_3 = baker.make(Comment, post=private_post, user=admin, content=fake.text())

    # comment_3 = baker.make(Comment, post=post, user=no_user, content=fake.text())
    post = baker.make(Post, author=admin, content=fake.text(), is_published=True)

    return { "post": post, "super_comment": comment, "normal_comment": comment_2, "private_post": private_post, "private_comment": comment_3}

@pytest.fixture
def liked_objects(objects):
    post = objects['post']
    super_comment = objects['super_comment']
    normal_comment = objects['normal_comment']

    post_type = ContentType.objects.get_for_model(post)
    super_comment_type = ContentType.objects.get_for_model(super_comment)
    normal_comment_type = ContentType.objects.get_for_model(normal_comment)

    baker.make(Like, content_type=post_type, object_id=post.pk, user=post.author)
    baker.make(Like, content_type=post_type, object_id=post.pk, user=normal_comment.user)

    super_comment_like = baker.make(Like, content_type=super_comment_type, object_id=super_comment.pk, user=super_comment.user)
    normal_comment_like = baker.make(Like, content_type=normal_comment_type, object_id=normal_comment.pk, user=normal_comment.user)

    return { "post": post, "super_comment": super_comment, "normal_comment": normal_comment, 'super_comment_like': super_comment_like, 'normal_comment_like': normal_comment_like}

@pytest.fixture
def authenticate():
    def _authenticate(user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    return _authenticate

@pytest.fixture
def apply_like(authenticate):
    def _apply_like(user, content_type, object_id):
        client = authenticate(user)
        data = {"content_type": content_type, "object_id": object_id}
        response = client.post(reverse('like-list'), data)
        return response

    return _apply_like

@pytest.fixture
def get_likes(authenticate):
    def _get_likes(user):
        client = authenticate(user)
        response = client.get(reverse('like-list'))
        return response

    return _get_likes

@pytest.fixture
def like_data():
    user = User.objects.create_user(username='testuser', password='testpassword')
    other_user = User.objects.create_user(username='otheruser', password='otherpassword')
    comment = Comment.objects.create(text='Test Comment')
    like = Like.objects.create(user=other_user, content_object=comment)
    return user,like
