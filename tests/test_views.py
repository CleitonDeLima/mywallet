import pytest
from django.shortcuts import resolve_url
from django.utils import timezone

from core.models import Transaction


def test_home(logged_client):
    url = resolve_url("core:home")
    response = logged_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
class TestTransactions:
    def test_get_list(self, user, logged_client, transaction_factory):
        transaction = transaction_factory(wallet__user=user)
        url = resolve_url("core:transaction-list")
        response = logged_client.get(url)
        assert response.status_code == 200
        assert list(response.context["transaction_list"]) == [transaction]

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
