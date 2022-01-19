import logging
from decimal import ROUND_UP, Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from pandas_datareader._utils import RemoteDataError
from pandas_datareader.data import DataReader

from core.models import Ticker

logger = logging.getLogger(__name__)


def decimal(value) -> Decimal:
    return Decimal(value).quantize(Decimal("0.00"), ROUND_UP)


def retrieve_close_price(asset) -> Decimal:
    """
    Looking last price
    """
    today = timezone.now().today()

    name = f"{asset}.SA"
    source = "yahoo"
    logger.debug(f"Looking up the ticker {name} from {source}.")

    df = DataReader(
        name,
        source,
        start=today - timezone.timedelta(30),
        end=today,
    )
    df = df.tail(1)
    float_price = float(df["Close"])
    price = decimal(float_price)
    return price


class Command(BaseCommand):
    help = "Updates stock price via yahoo finances"

    def handle(self, *args, **options):
        tickers = []

        for ticker in Ticker.objects.all():
            try:
                ticker.price = retrieve_close_price(ticker.name)
            except RemoteDataError:
                self.stdout.write(self.style.ERROR(f"{ticker.name} not found."))
                continue

            ticker.updated_at = timezone.now()
            tickers.append(ticker)

        rows_updated = Ticker.objects.bulk_update(
            tickers,
            ["price", "updated_at"],
        )
        message = f"{rows_updated} updated tickets."
        self.stdout.write(self.style.SUCCESS(message))
