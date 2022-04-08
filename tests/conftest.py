import pytest
from pytest_factoryboy import register

from tests.factories import (
    TickerFactory,
    TransactionFactory,
    UserFactory,
    WalletFactory,
)

register(UserFactory)
register(TickerFactory)
register(WalletFactory)
register(TransactionFactory)


@pytest.fixture
def user(db, django_user_model, django_username_field):
    UserModel = django_user_model
    username_field = django_username_field
    username = "user@example.com" if username_field == "email" else "user"

    try:
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        user_data = {}
        if "email" in UserModel.REQUIRED_FIELDS:
            user_data["email"] = "user@example.com"
        user_data["password"] = "password"
        user_data[username_field] = username
        user = UserModel._default_manager.create_superuser(**user_data)
    return user


@pytest.fixture
def logged_client(user, client):
    client.force_login(user)
    return client
