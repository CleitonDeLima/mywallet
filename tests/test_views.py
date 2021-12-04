import pytest
from django.shortcuts import resolve_url

from core.models import StockAsset, Ticket, Wallet


def test_home(client):
    url = resolve_url("core:home")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
class TestWallet:
    def test_get_list(self, client):
        w1 = Wallet.objects.create(name="wallet 1")
        w2 = Wallet.objects.create(name="wallet 2")
        url = resolve_url("core:wallet-list")
        response = client.get(url)
        assert response.status_code == 200
        assert list(response.context["wallet_list"]) == [w1, w2]

    def test_get_create(self, client):
        url = resolve_url("core:wallet-create")
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestAssets:
    def test_get_list(self, client):
        t = Ticket.objects.create(name="t", price=100, type=Ticket.Types.ACAO)
        w = Wallet.objects.create(name="wallet 1")
        s = StockAsset.objects.create(
            ticket=t,
            wallet=w,
            quantity=10,
            expected_allocation=10,
        )
        url = resolve_url("core:asset-list")
        response = client.get(url)
        assert response.status_code == 200
        assert list(response.context["asset_list"]) == [s]

    def test_get_list_by_wallet(self, client):
        t1 = Ticket.objects.create(name="t", price=100, type=Ticket.Types.ACAO)
        t2 = Ticket.objects.create(name="t", price=100, type=Ticket.Types.ACAO)
        w = Wallet.objects.create(name="wallet 1")
        StockAsset.objects.create(
            ticket=t1,
            wallet=w,
            quantity=10,
            expected_allocation=10,
        )
        StockAsset.objects.create(
            ticket=t2,
            quantity=10,
            expected_allocation=10,
        )
        url = resolve_url("core:asset-list", wallet_id=w.id)
        response = client.get(url)
        assert response.status_code == 200
        assert list(response.context["asset_list"]) == list(w.assets.all())

    def test_list_assets_to_buy(self, client):
        w = Wallet.objects.create(name="wallet 1")
        url = resolve_url("core:rebalancing", wallet_id=w.id)
        response = client.get(url)
        assert response.status_code == 200
