import pytest
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from tags.models import TaggedItem
from django.apps import apps

@pytest.mark.django_db
class TestTaggedItemViewSet:
#
    @pytest.mark.parametrize('role', ['admin', 'user', 'non_user'])
    def test_list_tagged_items(self, clients, tagged_items, role):
        api_client = clients[role]
        url = reverse('taggeditem-list')

        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == len(tagged_items)

    @pytest.mark.parametrize('role, status, expected_increase', [('admin', 201, 1), ('user', 403, 0), ('non_user', 401, 0)])
    def test_create_tagged_item(self, clients, tagged_items, role, status, expected_increase):
        api_client = clients[role]
        url = reverse('taggeditem-list')
        tagged_item = tagged_items[0]
        model_name = tagged_item.content_type.model
        label = "New Label"
        data = {"label": label, "content_type": model_name, "object_id": tagged_item.object_id}
        tags_count_before = tagged_item.tags.count()

        print("Create data:", data)
        response = api_client.post(url, data=data)
        # tags_count_after = tagged_item.tag.count()

        assert response.status_code == status

        if role == 'admin':
            # tagged_item = TaggedItem.objects.get(id=tagged_item.id)
            tags = tagged_item.tags.values_list('label', flat=True)
            assert label in tags
            assert len(tags) == tags_count_before + 1

    @pytest.mark.parametrize('role', ['admin', 'user', 'non_user'])
    def test_retrieve_tagged_item(self, clients, tagged_items, role):
        api_client = clients[role]
        tagged_item = tagged_items[0]
        url = reverse('taggeditem-detail', args=[tagged_item.pk])
        tagged_item = tagged_items[0]

        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['id'] == tagged_item.pk
        # assert response.data['tag'] == tagged_item.tag
        assert len(response.data['tags']) == tagged_item.tags.count()

    # @pytest.mark.parametrize('role', ['admin', 'user', 'non_user'])
    # def test_update_tagged_item(self, clients, role, tagged_items, tags):
    #     tagged_item = tagged_items[0]
    #     api_client = clients[role]
    #     url = reverse('taggeditem-detail', args=[tagged_item.pk])

    #     data = {
    #         "name": "updated_item",
    #         "tags": [tags[1].pk, tags[2].pk]
    #     }

    #     response = api_client.put(url, data=data)

    #     assert response.status_code == 200
    #     assert response.data['name'] == data['name']
    #     assert len(response.data['tags']) == len(data['tags'])

    @pytest.mark.parametrize('role, status, expected_decrease', [('admin', 204, 1), ('user', 403, 0), ('non_user', 401, 0)])
    def test_delete_tagged_item_all_tags_remove(self, clients, tagged_items, role, status, expected_decrease):
        tagged_item = tagged_items[0]
        api_client = clients[role]
        url = reverse('taggeditem-detail', args=[tagged_item.id])

        response = api_client.delete(url)

        assert response.status_code == status
        if role == 'admin':
            assert TaggedItem.objects.filter(id=tagged_item.id).count() == 0
            # assert Tag.objects.filter(label__in=tagged_item.tag.name()).count() == expected_decrease

    @pytest.mark.parametrize('role, status', [('admin', 201), ('user', 403), ('non_user', 401)])
    def test_if_add_tag_to_tagged_item_then_remove(self, clients, tagged_items, tags, role, status):
        tagged_item = tagged_items[0]
        new_label = "Example"
        # new_tag = Tag(label=new_label)
        # tagged_item.tag.add(new_tag)
        model_name = tagged_item.content_type.model
        api_client = clients[role]

        url = reverse('taggeditem-list')
        data = {"label": new_label, 'content_type': model_name, 'object_id': tagged_item.object_id}

        response = api_client.post(url, data=data)
        print("Add tag:", response.json())
        # assert response.status_code == status

        response2 = api_client.post(url, data=data)
        print("Add tag:", response.json())
        assert response2.status_code == status

        if role == 'admin':
            assert new_label not in tagged_item.tags.all()

