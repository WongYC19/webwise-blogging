import os
from itertools import product

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient

from tags.models import Tag, TaggedItem, DummyModel

User = get_user_model()

@pytest.fixture
def clients():
    admin = User.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword'
    )

    user = User.objects.create_user(
        email='user@example.com',
        password='userpassword'
    )

    users = {
        "admin": admin,
        "user": user,
        "non_user": None,
    }

    api_clients = {}
    for role, user in users.items():
        client = APIClient()
        if user:
            client.force_authenticate(user=user)
        api_clients[role] = client
    # api_clients = {role: APIClient().force_authenticate(user) for role, user in users.items()}
    return api_clients

@pytest.fixture
def tags():
    tag_names = ["Python", "Django", "Flask"]
    tag_list = []
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(label=tag_name)
        tag_list.append(tag)
    return tag_list

@pytest.fixture
def dummies():
    # Create some dummy objects
    dummies_list = []
    for i in range(1, 4):
        dummy = DummyModel.objects.create(name=f'Dummy {i}')
        dummy.save()
        dummies_list.append(dummy)

    return dummies_list

@pytest.fixture
def tagged_items(tags, dummies):
    tagged_items_list = []
    for tag, dummy in product(tags, dummies):
        print("Dummy:", dummy)
        content_type = ContentType.objects.get_for_model(dummy)
        tagged_item = TaggedItem.objects.create(
            content_type=content_type,
            object_id=str(dummy.pk),
            content_object=dummy
        )
        tagged_item.tags.add(tag)
        tagged_items_list.append(tagged_item)

    return tagged_items_list
