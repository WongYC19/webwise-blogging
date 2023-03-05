import pytest
from django.urls import reverse
from tags.models import Tag

@pytest.mark.django_db
class TestTag:

    @pytest.mark.parametrize('user, status', [
        ('admin', 200),
        ('user', 200),
        ('non_user', 200),
    ])
    def test_view_tag(self, clients, user, status, tags):
        url = reverse('tag-list')
        api_client = clients[user]

        response = api_client.get(url)

        assert response.status_code == status
        assert len(response.data) == len(tags)

    @pytest.mark.parametrize('user, status, increased', [
        ('admin', 201, 1),
        ('user', 403, 0),
        ('non_user', 401, 0),
    ])
    def test_create_tag(self, clients, user, status, increased, tags):
        url = reverse('tag-list')
        api_client = clients[user]

        response = api_client.post(url, data={'label': user})
        assert response.status_code == status

        after_count = Tag.objects.count()
        assert after_count - len(tags) == increased

    def test_duplicate_tag(self, clients):
        api_client = clients['admin']
        url = reverse('tag-list')
        label = 'Testing label'

        response = api_client.post(url, data={"label": label})

        before_duplicate_count = Tag.objects.count()
        response2 = api_client.post(url, data={"label": label})
        after_duplicate_count = Tag.objects.count()

        assert response2.status_code == 400
        assert after_duplicate_count == before_duplicate_count

