import pytest
from rest_framework import status

@pytest.mark.django_db(transaction=False)
class TestComment:

    def test_if_normal_user_comment_on_private_post_return_403(self, user_data, create_comment, comment_data):
        user = user_data(False)

        response = create_comment(user, is_published=False, content=comment_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_comment_on_public_post_return_201(self, user_data, create_comment, comment_data):
        user = user_data(False)

        response = create_comment(user, is_published=True, content=comment_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == comment_data

    def test_if_admin_create_comment_on_private_post_return_201(self, user_data, create_comment, comment_data):
        user = user_data(True)

        response = create_comment(user, is_published=False, content=comment_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == comment_data

    def test_if_admin_create_comment_on_public_post_return_201(self, user_data, create_comment, comment_data):
        user = user_data(True)

        response = create_comment(user, is_published=True, content=comment_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == comment_data

    def test_if_anonymous_user_create_comment_on_private_post_return_401(self, user_data, create_comment, comment_data):
        user = user_data(None)

        response = create_comment(user, is_published=False, content=comment_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_anonymous_user_create_comment_on_public_post_return_403(self, user_data, create_comment, comment_data):
        user = user_data(None)

        response = create_comment(user, is_published=True, content=comment_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_admin_edit_comment_on_private_post_return_200(self, user_data, edit_comment, comment_data):
        user = user_data(True)

        response = edit_comment(user, is_published=False, content=comment_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == comment_data

    def test_if_admin_edit_comment_on_public_post_return_200(self, user_data, edit_comment, comment_data):
        user = user_data(True)

        response = edit_comment(user, is_published=True, content=comment_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == comment_data

    def test_if_normal_user_edit_comment_on_private_post_return_403(self, user_data, create_comment, edit_comment, comment_data):
        user = user_data(False)
        admin = user_data(True)
        comment_response = create_comment(admin, is_published=False, content=comment_data)

        data = comment_response.data
        comment_id = data['pk']
        post_id = data['post']

        response = edit_comment(user, comment_id=comment_id, post_id=post_id, content = comment_data, is_published=False)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_edit_comment_on_public_post_return_200(self, user_data, edit_comment, comment_data):
        user = user_data(False)

        response = edit_comment(user, content = comment_data, is_published=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == comment_data

    def test_if_user_edit_comment_they_do_not_own_return_403(self, user_data, create_comment, edit_comment):
        owner = user_data(is_staff=False)
        other_user = user_data(is_staff=False)
        comment = create_comment(owner, is_published=True)
        comment_id = comment.data['pk']
        post_id = comment.data['post']

        response = edit_comment(other_user, post_id=post_id, comment_id=comment_id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_delete_comment_on_private_post_return_200(self, user_data, delete_comment):
        user = user_data(True)

        response = delete_comment(user, is_published=False)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_admin_delete_comment_on_public_post_return_200(self, user_data, delete_comment):
        user = user_data(True)

        response = delete_comment(user, is_published=True)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_normal_user_delete_comment_on_private_post_return_403(self, user_data, create_comment, delete_comment):
        user = user_data(False)
        admin = user_data(True)

        create_response = create_comment(admin, is_published=False)
        data = create_response.data
        comment_id = data['pk']
        post_id = data['post']

        response = delete_comment(user, post_id=post_id, comment_id=comment_id, is_published=False)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_delete_comment_on_public_post_return_403(self, user_data, create_comment, delete_comment):
        user = user_data(False)
        admin = user_data(True)

        create_response = create_comment(admin, is_published=True)
        data = create_response.data
        comment_id = data['pk']
        post_id = data['post']

        response = delete_comment(user, post_id=post_id, comment_id=comment_id, is_published=True)

        assert response.status_code == status.HTTP_403_FORBIDDEN



