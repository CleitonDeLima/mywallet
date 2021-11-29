import logging
from decimal import ROUND_UP, Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from pandas_datareader.data import DataReader

from core.models import Ticket

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
    logger.debug(f"Looking up the ticket {name} from {source}.")

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
        tickets = []

        for ticket in Ticket.objects.all():
            ticket.price = retrieve_close_price(ticket.name)
            ticket.updated_at = timezone.now()
            tickets.append(ticket)

        rows_updated = Ticket.objects.bulk_update(
            tickets,
            ["price", "updated_at"],
        )
        message = f"{rows_updated} updated tickets."
        self.stdout.write(self.style.SUCCESS(message))
