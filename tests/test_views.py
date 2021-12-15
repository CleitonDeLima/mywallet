import pytest
from django.shortcuts import resolve_url
from django.utils import timezone

from core.models import Transaction, Wallet


def test_home(logged_client):
    url = resolve_url("core:home")
    response = logged_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
class TestWallet:
    def test_get_list(self, logged_client, wallet_factory):
        w1 = wallet_factory()
        w2 = wallet_factory()
        url = resolve_url("core:wallet-list")
        response = logged_client.get(url)
        assert response.status_code == 200
        assert list(response.context["wallet_list"]) == [w1, w2]

    def test_get_create(self, logged_client):
        url = resolve_url("core:wallet-create")
        response = logged_client.get(url)
        assert response.status_code == 200

    def test_post_create(self, logged_client):
        url = resolve_url("core:wallet-create")
        data = {"name": "wallet1"}
        response = logged_client.post(url, data)
        assert response.status_code == 302
        assert Wallet.objects.count() == 1

    def test_post_update(self, logged_client):
        w = Wallet.objects.create(name="wallet 1")
        url = resolve_url("core:wallet-update", w.id)
        data = {"name": "wallet updated"}
        response = logged_client.post(url, data)
        w.refresh_from_db()
        assert response.status_code == 302
        assert w.name == "wallet updated"


@pytest.mark.django_db
class TestTransactions:
    def test_get_list(self, logged_client, transaction):
        url = resolve_url("core:transaction-list")
        response = logged_client.get(url)
        assert response.status_code == 200
        assert list(response.context["transaction_list"]) == [transaction]

    def test_get_list_by_wallet(self, logged_client, transaction_factory):
        t = transaction_factory()
        transaction_factory(wallet=None)
        url = resolve_url("core:transaction-list", wallet_id=t.wallet.id)
        response = logged_client.get(url)

        assert response.status_code == 200
        assert list(response.context["transaction_list"]) == list(
            t.wallet.transactions.all()
        )

    def test_get_create(self, logged_client, wallet):
        url = resolve_url("core:transaction-create")
        response = logged_client.get(url)
        assert response.status_code == 200

    def test_post_create(self, logged_client, ticker, wallet):
        url = resolve_url("core:transaction-create")
        data = {
            "wallet": wallet.id,
            "ticker": ticker.id,
            "quantity": 5,
            "price": 10,
            "date": timezone.localdate(),
            "order": Transaction.OrderTypes.BUY,
        }
        response = logged_client.post(url, data)
        assert response.status_code == 302
        assert Transaction.objects.count() == 1

    def test_update(self, logged_client, transaction):
        url = resolve_url(
            "core:transaction-update",
            transaction.id,
        )
        response = logged_client.get(url)
        assert response.status_code == 200

        data = {
            "wallet": transaction.wallet.id,
            "ticker": transaction.ticker.id,
            "quantity": 10,
            "price": 10,
            "date": timezone.localdate(),
            "order": Transaction.OrderTypes.SELL,
        }
        response = logged_client.post(url, data)
        assert response.status_code == 302
