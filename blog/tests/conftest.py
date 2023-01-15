import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from faker import Faker
from model_bakery import baker
from ..models import Post, Comment

User = get_user_model()
fake = Faker()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    def _user_data(is_staff=False):
        if is_staff is None:
            return None

        email = fake.email()
        password = fake.password(length=16, special_chars=True, digits=True, upper_case=True, lower_case=True)
        user = baker.prepare(User, email=email, password=password, is_superuser=is_staff, is_staff=is_staff)
        user.save()
        return user
    return _user_data

@pytest.fixture
def authenticate(api_client):
    def _authenticate(user):
        api_client.force_authenticate(user=user)
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
def create_post_instance():
    def _create_post_instance(user, quantity, is_published=False):
        posts = baker.make(Post, _quantity=quantity, is_published=is_published, author=user)
        return posts
    return _create_post_instance

@pytest.fixture
def comment_data():
    content = fake.text()
    return content

@pytest.fixture
def get_posts(api_client, authenticate):
    def _get_posts(user):
        authenticate(user)
        return api_client.get(f'/blog/posts/')
    return _get_posts

@pytest.fixture
def get_post(api_client, authenticate):
    def _get_post(user, post_id):
        authenticate(user)
        return api_client.get(f'/blog/posts/{post_id}/')
    return _get_post

@pytest.fixture
def create_post(api_client, authenticate, post_data):
    def _create_post(user, title = None, content = None, is_published = False):
        data = post_data(title=title, content=content, is_published=is_published)
        print("Data:", data)
        authenticate(user)
        return api_client.post('/blog/posts/', data)
    return _create_post

@pytest.fixture
def edit_post(authenticate, post_data):
    def _edit_post(user, post_id, title = None, content = None, is_published = False):
        data = post_data(title=title, content=content, is_published=is_published)
        authenticate(user)
        return api_client.put(f'/blog/posts/{post_id}/', data)
    return _edit_post

@pytest.fixture
def delete_post(api_client, authenticate):
    def _delete_post(user, post_id):
        authenticate(user)
        return api_client.delete(f'/blog/posts/{post_id}/')
    return _delete_post

@pytest.fixture
def get_comments_from_post(api_client, authenticate):
    def _get_comments_from_post(user, post_id):
        authenticate(user)
        return api_client.get(f'/blog/posts/{post_id}/comments/')
    return _get_comments_from_post

@pytest.fixture
def create_comment(api_client, user_data, authenticate, create_post, comment_data):
    def _create_comment(user, is_published=False, content=None):
        admin = user_data(True)
        post = create_post(admin, is_published=is_published)
        post_id = post.data['pk']

        authenticate(user)

        content = content or comment_data
        return api_client.post(f'/blog/posts/{post_id}/comments/', {"content": content})
    return _create_comment

@pytest.fixture
def comment_instance(user_data, create_post_instance, comment_data):
    def _comment_instance(user, quantity=1, is_published=False):
        admin = user_data(True)
        posts = create_post_instance(admin, quantity=1, is_published=is_published)
        post = posts[0]
        data = {"content": comment_data, "post": post, "user": user}
        comment = baker.make(Comment, _quantity=quantity, **data)
        return comment

    return _comment_instance

@pytest.fixture
def edit_comment(api_client, authenticate, create_comment, comment_data):
    def _edit_comment(user, post_id = None, comment_id=None, content = None, is_published=False):
        authenticate(user)

        if comment_id is None or post_id is None:
            response = create_comment(user, content=content, is_published=is_published)
            data = response.data
            comment_id = data['pk']
            post_id = data['post']

        content = content or comment_data

        return api_client.put(f'/blog/posts/{post_id}/comments/{comment_id}/', {"content": content})

    return _edit_comment

@pytest.fixture
def delete_comment(api_client, authenticate, create_comment):
    def _delete_comment(user, comment_id=None, post_id=None, is_published = False):
        authenticate(user)

        if comment_id is None or post_id is None:
            comment = create_comment(user, is_published=is_published)
            comment_id = comment.data['pk']
            post_id = comment.data['post']

        return api_client.delete(f'/blog/posts/{post_id}/comments/{comment_id}/')

    return _delete_comment

