import factory
from django.conf import settings
from django.utils import timezone
from faker import Factory as FakerFactory

from core.models import Ticker, Transaction, Wallet

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ["email"]

    username = factory.LazyAttribute(lambda x: faker.name())
    email = "user@test.com"


class TickerFactory(factory.django.DjangoModelFactory):
    """Ticker factory."""

    class Meta:
        model = Ticker

    name = factory.LazyAttribute(lambda x: faker.cryptocurrency_code())
    price = 99.90
    type = Ticker.Types.ACAO


class WalletFactory(factory.django.DjangoModelFactory):
    """Wallet factory."""

    class Meta:
        model = Wallet

    name = factory.LazyAttribute(lambda x: faker.name())
    user = factory.SubFactory(UserFactory)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    ticker = factory.SubFactory(TickerFactory)
    wallet = factory.SubFactory(WalletFactory)
    quantity = 10
    price = 1
    date = factory.LazyFunction(timezone.localdate)
    order = Transaction.OrderTypes.BUY
