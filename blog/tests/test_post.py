import pytest
from blog.models import Post
@pytest.mark.django_db(transaction=False)
class TestPost:

    @pytest.mark.parametrize("user_type, is_published, status_code", [
        ('superuser', False, 201),
        ('normal_user', False, 403),
        ('anonymous_user', False, 401),
        ('superuser', True, 201),
        ('normal_user', True, 403),
        ('anonymous_user', True, 401),
    ])
    def test_if_user_create_post(self, create_post, user_type, is_published, status_code):
        response = create_post(user_type, is_published=is_published)

        assert response.status_code == status_code

    @pytest.mark.parametrize("user_type, title, content, post_type, status_code", [
        ('superuser', None, None, "private", 200),
        ('normal_user', None, None, "private", 403),
        ('anonymous_user', None, None, "private", 401),
        ('superuser', "", None, "private", 400),
        ('superuser', None, "", "private", 400),
        ('superuser', None, None, "public", 200),
        ('normal_user', None, None, "public", 403),
        ('anonymous_user', None, None, "public", 401),
        ('superuser', "", None, "public", 400),
        ('superuser', None, "", "public", 400),
    ])
    def test_if_user_edit_post(self, edit_post, user_type, post_type, title, content, status_code):
        response = edit_post(user_type, post_type, title, content)

        assert response.status_code == status_code

    @pytest.mark.parametrize("title, content, is_published, status_code", [
        ("", None, True, 400),
        ("", None, False, 400),
        (None, "", True, 400),
        (None, "", False, 400),
        ("22", None, True, 400),
        ("22", None, False, 400),
        (None, "22", True, 400),
        (None, "22", False, 400),
        (None, None, True, 201),
        (None, None, False, 201),
    ])
    def test_invalid_values_create_post(self, create_post, title, content, is_published, status_code):
        response = create_post("superuser", title, content, is_published)

        assert response.status_code == status_code

    @pytest.mark.parametrize("user_type, status_code", [
        ('superuser', 200),
        ('normal_user', 200),
        ('anonymous_user', 200),
    ])
    def test_if_user_list_posts(self, get_posts, user_type, status_code):
        response = get_posts(user_type)

        assert response.status_code == status_code

        if user_type == 'superuser':
            assert len(response.data['results']) == Post.objects.count()
        else:
            assert len(response.data['results']) == Post.objects.filter(is_published=True).count()

    @pytest.mark.parametrize("user_type, status_code, post_type", [
        ('superuser', 200, 'private'),
        ('normal_user', 404, 'private'),
        ('anonymous_user', 404, 'private'),
        ('superuser', 200, 'public'),
        ('normal_user', 200, 'public'),
        ('anonymous_user', 200, 'public'),
    ])
    def test_if_user_retrieve_post(self, get_post, posts, user_type, status_code, post_type):
        post = posts[post_type]

        response = get_post(user_type, post.pk)

        assert response.status_code == status_code

    @pytest.mark.parametrize("user_type, status_code, post_type", [
        ('superuser', 204, 'private'),
        ('normal_user', 403, 'private'),
        ('anonymous_user', 401, 'private'),
        ('superuser', 204, 'public'),
        ('normal_user', 403, 'public'),
        ('anonymous_user', 401, 'public'),
    ])
    def test_if_user_delete_post(self, delete_post, posts, user_type, status_code, post_type):
        post = posts[post_type]

        response = delete_post(user_type, post.pk)

        assert response.status_code == status_code