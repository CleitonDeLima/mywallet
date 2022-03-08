import factory
from django.utils import timezone
from faker import Factory as FakerFactory

from core.models import Ticker, Transaction, Wallet, WalletItem

faker = FakerFactory.create()


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


class WalletItemFactory(factory.django.DjangoModelFactory):
    """WalletItem factory."""

    class Meta:
        model = WalletItem

    wallet = factory.SubFactory(WalletFactory)
    ticker = factory.SubFactory(TickerFactory)
    started_in = None
    closed_in = None
    allocation = 5
    entry_price = 10
    ceiling_price = 20


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    ticker = factory.SubFactory(TickerFactory)
    wallet = factory.SubFactory(WalletFactory)
    quantity = 10
    price = 1
    date = factory.LazyFunction(timezone.localdate)
    order = Transaction.OrderTypes.BUY
