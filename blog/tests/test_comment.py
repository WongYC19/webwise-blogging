import pytest
from rest_framework import status

@pytest.mark.django_db(transaction=False)
class TestComment:

    @pytest.mark.parametrize("user, is_published, status_code", [
        ("anonymous_user", "private", 401),
        ("normal_user", "private", 403),
        ("superuser", "private", 201),
        ("anonymous_user", "public", 401),
        ("normal_user", "public", 201),
        ("superuser", "public", 201),
    ])
    def test_if_user_create_comment_on_post(self, create_comment, user, is_published, status_code):
        response = create_comment(user, is_published)

        assert response.status_code == status_code

    @pytest.mark.parametrize("user_type, comment_type, status_code", [
        ("superuser", "super_private", 200),
        ("normal_user", "normal_private", 403),
        ("superuser", "super_public", 200),
        ("normal_user", "normal_public", 200),
        ("anonymous_user", "normal_public", 401),
        ("anonymous_user", "super_public", 401),
    ])
    def test_if_user_edit_comment_on_post(self, user_type, edit_comment, comments, comment_type, status_code):
        comment = comments[comment_type]
        comment_id = comment.pk
        post_id = comment.post.pk

        response = edit_comment(user_type, post_id, comment_id)

        assert response.status_code == status_code

    @pytest.mark.parametrize("user_type, comment_type, status_code", [
        ("superuser", "super_private", 204),
        ("normal_user", "normal_private", 403),
        ("superuser", "super_public", 204),
        ("normal_user", "normal_public", 204),
        ("anonymous_user", "normal_public", 401),
        ("anonymous_user", "super_public", 401),
    ])
    def test_if_user_delete_comment_on_post(self, delete_comment, user_type, comments, comment_type, status_code):
        comment = comments[comment_type]
        comment_id = comment.pk
        post_id = comment.post.pk

        response = delete_comment(user_type, comment_id, post_id)

        assert response.status_code == status_code

    @pytest.mark.parametrize("user_type, post_type, status_code", [
        ("superuser", "private", 200),
        ("normal_user", "private", 403),
        ("anonymous_user", "private", 401),
        ("superuser", "public", 200),
        ("normal_user", "public", 200),
        ("anonymous_user", "public", 401),
    ])
    def test_if_user_read_comment_on_post(self, read_comments, posts, user_type, post_type, status_code):
        post = posts[post_type]

        response = read_comments(user_type, post.pk)

        assert response.status_code == status_code
