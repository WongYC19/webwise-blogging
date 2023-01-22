from django.urls import reverse
from django.contrib.auth import get_user_model

import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIClient

from ..models import Post, Comment

User = get_user_model()
fake = Faker()

posts_url = reverse('posts-list')

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def users():
    email = lambda: fake.email()
    password = lambda: fake.password(length=16, special_chars=True, digits=True, upper_case=True, lower_case=True)
    superuser = User.objects.create_superuser(email(), password())
    normal_user = User.objects.create_user(email(), password())

    users = {
        "superuser": superuser,
        "normal_user": normal_user,
        "anonymous_user": None,
    }

    return users

@pytest.fixture
def authenticate(api_client):
    def _authenticate(user):
        return api_client.force_authenticate(user=user)
    return _authenticate

@pytest.fixture
def post_data():
    def _post_data(title = None, content = None, is_published=False):
        if title is None:
            title = fake.sentence()

        if content is None:
            content = fake.text()
        return dict(title=title, content=content, is_published=is_published)
    return _post_data

@pytest.fixture
def posts(users, post_data):
    private = Post.objects.create(author=users['superuser'], **post_data(is_published=False))
    public = Post.objects.create(author=users['superuser'], **post_data(is_published=True))
    print("All posts:", Post.objects.all())
    return {
        "private": private,
        "public": public,
    }

@pytest.fixture
def get_posts(api_client, users, authenticate, posts):
    def _get_posts(user_type):
        authenticate(users[user_type])
        return api_client.get(posts_url)
    return _get_posts

@pytest.fixture
def get_post(api_client, users, authenticate):
    def _get_post(user_type, post_id):
        authenticate(users[user_type])
        url = reverse("posts-detail", kwargs={"pk": post_id})
        return api_client.get(url)
    return _get_post

@pytest.fixture
def create_post(api_client, authenticate, users):
    def _create_post(user_type, title = None, content = None, is_published=False):
        authenticate(users[user_type])

        title = fake.sentence() if title is None else ""
        content = fake.text() if content is None else ""

        data = {"title": title, "content": content, "is_published":is_published}
        return api_client.post(posts_url, data)
    return _create_post

@pytest.fixture
def edit_post(api_client, users, authenticate, posts):
    def _edit_post(user_type, post_type, title = None, content = None):
        post = posts[post_type]
        post_id = post.pk
        title = fake.sentence() if title is None else ""
        content = fake.text() if content is None else ""
        data = {"title": title, "content": content}
        authenticate(users[user_type])
        url = reverse("posts-detail", kwargs={"pk": post_id})
        return api_client.put(url, data)
    return _edit_post

@pytest.fixture
def delete_post(api_client, users, authenticate):
    def _delete_post(user_type, post_id):
        authenticate(users[user_type])
        url = reverse('posts-detail', kwargs={'pk': post_id})
        return api_client.delete(url)
    return _delete_post

@pytest.fixture
def read_comments(api_client, users, authenticate):
    def _get_comments_from_post(user_type, post_id):
        authenticate(users[user_type])
        url = reverse('post-comments-list', kwargs={"post_pk": post_id})
        return api_client.get(url)
    return _get_comments_from_post

@pytest.fixture
def create_comment(api_client, users, posts, authenticate):
    def _create_comment(user_type, post_type):
        user = users[user_type]
        authenticate(user)

        post = posts[post_type]
        post_id = post.pk
        content = fake.text()

        url = reverse('post-comments-list', kwargs={"post_pk": post_id})
        return api_client.post(url, {"content": content})

    return _create_comment

@pytest.fixture
def comments(users, posts):
    return {
        "super_private": baker.make(Comment, user=users['superuser'] , post=posts['private'], content=fake.sentence()),
        "normal_private": baker.make(Comment, user=users['normal_user'] , post=posts['private'], content=fake.sentence()),
        "super_public": baker.make(Comment, user=users['superuser'] , post=posts['public'], content=fake.sentence()),
        "normal_public": baker.make(Comment, user=users['normal_user'] , post=posts['public'], content=fake.sentence()),
    }

@pytest.fixture
def edit_comment(api_client, users, authenticate):
    def _edit_comment(user_type, post_id, comment_id):
        authenticate(users[user_type])
        content = fake.sentence()
        url = reverse('post-comments-detail', kwargs={"post_pk": post_id, "pk": comment_id})
        return api_client.put(url, {"content": content})

    return _edit_comment

@pytest.fixture
def delete_comment(api_client, users, authenticate, create_comment):
    def _delete_comment(user_type, comment_id, post_id):
        authenticate(users[user_type])
        url = reverse('post-comments-detail', kwargs={"post_pk": post_id, "pk": comment_id})
        return api_client.delete(url)

    return _delete_comment

