import pytest

@pytest.mark.django_db(transaction=False)
class TestLike:

    @pytest.mark.parametrize("user, key, content_type, status_code, increased_count",
        [
            ('anonymous_user', 'post', 'post', 401, 0),
            ('normal_user', 'post', 'post', 201, 1),
            ('superuser', 'post', 'post', 201, 1),
            ('anonymous_user', 'normal_comment',  'comment', 401, 0),
            ('normal_user', 'normal_comment', 'comment', 201, 1),
            ('superuser', 'super_comment', 'comment', 201, 1)
        ])
    def test_like_object(self, users, user, objects, key, content_type, status_code, increased_count, get_likes, apply_like):
        object = objects[key]
        like_count_before = get_likes(users[user]).data

        response = apply_like(users[user], content_type, object_id=object.pk)
        like_count_after = get_likes(users[user]).data

        assert response.status_code == status_code
        assert len(like_count_after) - len(like_count_before) == increased_count

    @pytest.mark.parametrize("user, key, content_type, status_code, decreased_count",
        [
            ('anonymous_user', 'post', 'post', 401, 0),
            ('normal_user', 'post', 'post', 204, -1),
            ('superuser', 'post', 'post', 204, -1),
            ('anonymous_user', 'normal_comment',  'comment', 401, 0),
            ('normal_user', 'normal_comment', 'comment', 204, -1),
            ('superuser', 'super_comment', 'comment', 204, -1)
        ])
    def test_unlike_object(self, users, user, key, content_type, status_code, decreased_count, liked_objects, get_likes, apply_like):
        object = liked_objects[key]
        like_count_before = get_likes(users[user]).data

        response = apply_like(users[user], content_type, object_id=object.pk)
        like_count_after = get_likes(users[user]).data

        assert response.status_code == status_code
        assert len(like_count_after) - len(like_count_before) == decreased_count

    @pytest.mark.parametrize("user, key, content_type, status_code",
        [
            ('anonymous_user', 'post', 'invalid', 401),
            ('normal_user', 'post', 'post2', 400),
            ('superuser', 'post', '222', 400),
            ('anonymous_user', 'normal_comment',  'invalid', 401),
            ('normal_user', 'normal_comment', 'post2', 400),
            ('superuser', 'super_comment', 'hehehe', 400)
        ])
    def test_invalid_content_types(self, users, user, key, content_type, status_code, objects, apply_like):
        object = objects[key]

        response = apply_like(users[user], content_type, object_id=object.pk)
        print("Response:", response.json())
        assert response.status_code == status_code

    @pytest.mark.parametrize("user, content, content_type, status_code",
        [
            ('superuser', 'private_post', 'post', 201),
            ('superuser', 'private_comment', 'comment', 201),
            ('normal_user', 'private_post', 'post', 403),
            ('normal_user', 'private_comment', 'comment', 403),
            ('anonymous_user', 'private_post', 'post', 401),
            ('anonymous_user', 'private_comment', 'comment', 401),
    ])
    def test_user_like_private_content(self, apply_like, objects, users, user, content, content_type, status_code):
        object = objects[content]

        response = apply_like(users[user], content_type, object.pk)

        assert response.status_code == status_code