import pytest
from django.shortcuts import resolve_url
from django.utils import timezone
from pytest_django.asserts import assertContains

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


@pytest.mark.django_db
class TestWalletAssets:
    def test_get(self, logged_client, wallet, transaction_factory):
        t1 = transaction_factory(wallet=wallet, ticker__name="AA", quantity=2)
        t2 = transaction_factory(wallet=wallet, ticker__name="AA", quantity=2)
        t3 = transaction_factory(wallet=wallet, ticker__name="BB", quantity=2)
        t4 = transaction_factory(
            wallet=wallet, ticker__name="BB", quantity=2, order="s"
        )
        t5 = transaction_factory(wallet=wallet, ticker__name="CC", quantity=3)
        # AA = 4
        # BB = 1
        # CC = 3
        url = resolve_url("core:wallet-assets", wallet.id)
        response = logged_client.get(url)
        assert response.status_code == 200
        assertContains(response, "<td>AA</td>", 1)
        assertContains(response, "<td>BB</td>", 0)
        assertContains(response, "<td>CC</td>", 1)


@pytest.mark.django_db
class TestWalletItems:
    def test_create(self, logged_client, wallet, ticker):
        data = {
            "wallet": wallet.id,
            "ticker": ticker.id,
            "started_in": None,
            "closed_in": None,
            "allocation": 5,
            "entry_price": 10,
            "ceiling_price": 20,
        }
        response = logged_client.get(
            resolve_url("core:walletitem-create", wallet.id)
        )
        assert response.status_code == 200
