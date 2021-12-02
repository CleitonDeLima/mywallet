import pytest
from django.shortcuts import resolve_url


def test_home(client):
    url = resolve_url("core:home")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_stock_asset_to_buy(client):
    url = resolve_url("core:stock-asset-to-buy")
    response = client.get(url)
    assert response.status_code == 200
