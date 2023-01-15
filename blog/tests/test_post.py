import pytest
from rest_framework import status
from model_bakery import baker

@pytest.mark.django_db(transaction=False)
class TestCreatePost:
    def test_if_anonymous_user_create_private_post_returns_401(self, user_data, create_post):
        user = user_data(None)

        response = create_post(user, is_published=False)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_anonymous_user_create_public_post_returns_401(self, user_data, create_post):
        user = user_data(None)

        response = create_post(user, is_published=True)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_normal_user_create_private_post_returns_403(self, user_data, create_post):
        user = user_data(False)

        response = create_post(user, is_published=False)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_create_public_post_returns_403(self, user_data, create_post):
        user = user_data(False)

        response = create_post(user, is_published=True)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_create_private_post_returns_201(self, user_data, create_post):
        user = user_data(True)

        response = create_post(user, is_published=False)

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_admin_create_public_post_returns_201(self, user_data, create_post):
        user = user_data(True)

        response = create_post(user, is_published=True)

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_title_empty_returns_returns_400(self, user_data, create_post):
        user = user_data(True)

        response = create_post(user, title="")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_content_empty_returns_returns_400(self, user_data, create_post):
        user = user_data(True)

        response = create_post(user, content="")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_is_published_empty_returns_201(self, user_data, create_post):
        user = user_data(True)

        response = create_post(user)

        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db(transaction=False)
class TestRetrievePost:

    def test_if_admin_get_private_post_return_200(self, user_data, create_post, get_post):
        user = user_data(True)
        post_response = create_post(user, is_published=False)

        new_post_id = post_response.data['pk']
        response = get_post(user, new_post_id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['pk'] == new_post_id

    def test_if_admin_get_public_post_return_200(self, user_data, create_post, get_post):
        user = user_data(True)
        post_response = create_post(user, is_published=False)

        new_post_id = post_response.data['pk']
        response = get_post(user, new_post_id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['pk'] == new_post_id

    def test_if_normal_user_get_private_post_return_404(self, user_data, create_post, get_post):
        user = user_data(False)
        admin = user_data(True)

        post_response = create_post(admin, is_published=False)
        new_post_id = post_response.data['pk']

        response = get_post(user, new_post_id)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_normal_user_get_public_post_return_200(self, user_data, create_post, get_post):
        user = user_data(False)
        admin = user_data(True)

        post_response = create_post(admin, is_published=True)
        new_post_id = post_response.data['pk']

        response = get_post(user, new_post_id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['pk'] == new_post_id

    def test_if_anonymous_get_private_post_return_404(self, user_data, create_post, get_post):
        user = user_data(None)
        admin = user_data(True)

        post_response = create_post(admin, is_published=False)
        new_post_id = post_response.data['pk']

        response = get_post(user, new_post_id)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_anonymous_get_public_post_return_200(self, user_data, create_post, get_post):
        user = user_data(None)
        admin = user_data(True)

        post_response = create_post(admin, is_published=True)
        new_post_id = post_response.data['pk']

        response = get_post(user, new_post_id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['pk'] == new_post_id

@pytest.mark.django_db(transaction=False)
class TestListPost:

    def test_if_admin_get_new_private_post_return_larger_list(self, user_data, create_post, get_posts):
        user = user_data(True)
        list_response = get_posts(user)
        ori_post_numbers = len(list_response.data)
        create_post(user, is_published=False)

        response = get_posts(user)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == ori_post_numbers + 1

    def test_if_admin_get_new_public_post_return_larger_list(self, user_data, create_post, get_posts):
        user = user_data(True)
        list_response = get_posts(user)
        ori_post_numbers = len(list_response.data)
        create_post(user, is_published=True)

        response = get_posts(user)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == ori_post_numbers + 1

    def test_if_normal_user_get_new_private_post_return_same_list(self, user_data, create_post, get_posts):
        user = user_data(False)
        admin = user_data(True)
        list_response = get_posts(user)
        ori_post_numbers = len(list_response.data)
        create_post(admin, is_published=False)

        response = get_posts(user)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == ori_post_numbers

    def test_if_normal_user_get_new_public_post_return_larger_list(self, user_data, create_post, get_posts):
        user = user_data(False)
        admin = user_data(True)
        list_response = get_posts(user)
        ori_post_numbers = len(list_response.data)
        create_post(admin, is_published=True)

        response = get_posts(user)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == ori_post_numbers + 1

    def test_if_anonymous_user_get_new_private_post_return_larger_list(self, user_data, create_post, get_posts):
        user = user_data(None)
        admin = user_data(True)
        list_response = get_posts(user)
        ori_post_numbers = len(list_response.data)
        create_post(admin, is_published=False)

        response = get_posts(user)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == ori_post_numbers

    def test_if_anonymous_user_get_new_public_post_return_larger_list(self, user_data, create_post, get_posts):
        user = user_data(None)
        admin = user_data(True)
        list_response = get_posts(user)
        ori_post_numbers = len(list_response.data)
        create_post(admin, is_published=True)

        response = get_posts(user)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == ori_post_numbers + 1

@pytest.mark.django_db(transaction=False)
class TestDeletePost:

    def test_if_admin_delete_private_post_return_204(self, user_data, create_post, delete_post):
        user = user_data(True)

        post_response = create_post(user, is_published=False)
        post_id = post_response.data['pk']

        response = delete_post(user, post_id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_admin_delete_public_post_return_204(self, user_data, create_post, delete_post):
        user = user_data(True)
        post_response = create_post(user, is_published=True)
        post_id = post_response.data['pk']

        response = delete_post(user, post_id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_normal_user_delete_private_post_return_403(self, user_data, create_post, delete_post):
        user = user_data(False)
        admin = user_data(True)
        post_response = create_post(admin, is_published=False)
        post_id = post_response.data['pk']

        response = delete_post(user, post_id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_normal_user_delete_public_post_return_403(self, user_data, create_post, delete_post):
        user = user_data(False)
        admin = user_data(True)
        post_response = create_post(admin, is_published=True)
        post_id = post_response.data['pk']

        response = delete_post(user, post_id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_delete_private_post_return_401(self, user_data, create_post, delete_post):
        user = user_data(None)
        admin = user_data(True)
        post_response = create_post(admin, is_published=False)
        post_id = post_response.data['pk']

        response = delete_post(user, post_id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_anonymous_user_delete_public_post_return_403(self, user_data, create_post, delete_post):
        user = user_data(None)
        admin = user_data(True)
        post_response = create_post(admin, is_published=True)
        post_id = post_response.data['pk']

        response = delete_post(user, post_id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED