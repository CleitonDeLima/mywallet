import factory
from django.utils import timezone
from faker import Factory as FakerFactory

from core.models import Ticker, Transaction, Wallet

faker = FakerFactory.create()


class WalletFactory(factory.django.DjangoModelFactory):
    """Wallet factory."""

    class Meta:
        model = Wallet

    name = factory.LazyAttribute(lambda x: faker.name())


class TickerFactory(factory.django.DjangoModelFactory):
    """Ticket factory."""

    class Meta:
        model = Ticker

    name = factory.LazyAttribute(lambda x: faker.cryptocurrency_code())
    price = 99.90
    type = Ticker.Types.ACAO


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    ticker = factory.SubFactory(TickerFactory)
    wallet = factory.SubFactory(WalletFactory)
    quantity = 10
    price = 1
    date = factory.LazyFunction(timezone.localdate)
    order = Transaction.OrderTypes.BUY
