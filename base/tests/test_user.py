from django.db.utils import IntegrityError

import pytest
from faker import Faker

from base.models import User

fake = Faker()

@pytest.fixture()
def user_data():
    return {
        "email": fake.email(),
        "password": fake.password(),
    }
@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self, user_data):
        email = user_data['email']
        password = user_data['password']
        user = User.objects.create_user(email=email, password=password)

        assert user.email == user_data['email']
        assert user.check_password(user_data['password']) is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self, user_data):
        email = user_data['email']
        password = user_data['password']
        user = User.objects.create_superuser(email=email, password=password)

        assert user.email == user_data['email']
        assert user.check_password(user_data['password']) is True
        assert user.is_staff is True
        assert user.is_superuser is True

    @pytest.mark.parametrize("attr", ['create_user', 'create_superuser'])
    def test_create_user_duplicate_email(self, user_data, attr):
        email = user_data['email']
        password = user_data['password']
        User.objects.__getattribute__(attr)(email=email, password=password)

        with pytest.raises(IntegrityError) as error:
            User.objects.create_superuser(email=email, password=password)
            assert "duplicate key value violates unique constraint" in str(error)

    @pytest.mark.parametrize("email, password, user_type", [
        ("", fake.password(), 'create_user'),
        # (fake.email(), "", 'create_user'),
        # (fake.sentence(), fake.password(), 'create_user'),
        ("", fake.password(), 'create_superuser'),
        # (fake.email(), "", 'create_superuser'),
        # (fake.sentence(), fake.password(), 'create_superuser'),
    ])
    def test_invalid_inputs(self, email, password, user_type):
        with pytest.raises(ValueError) as error:
            print(email, password, user_type)
            User.objects.__getattribute__(user_type)(email=email, password=password)
            assert str(error) in str(error)

