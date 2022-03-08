import argparse
import csv
import logging
from decimal import Decimal

from dateutil.parser import parse as parse_date
from django.core.management.base import BaseCommand

from core.forms import TransactionForm
from core.models import Ticker, Transaction, Wallet

logger = logging.getLogger(__name__)


def transform_to_decimal(value):
    digit_value = value.replace(",", "").replace(".", "")
    return Decimal(digit_value) / Decimal("100")


class Command(BaseCommand):
    help = "Updates stock price via yahoo finances"

    def add_arguments(self, parser) -> None:
        parser.add_argument("file", type=argparse.FileType("r"))
        parser.add_argument("wallet_name")

    def handle(self, *args, **options):
        file = options["file"]
        wallet_name = options["wallet_name"]

        wallet, created = Wallet.objects.get_or_create(name=wallet_name)
        if created:
            self.stdout.write(f"Wallet {wallet_name} created.")

        reader = csv.DictReader(file)
        objs = []
        for row in reader:
            ticker_name = row["ticker"]
            ticker_type = row["ticker_type"]
            ticker, created = Ticker.objects.get_or_create(
                name=ticker_name.upper(),
                defaults={
                    "type": ticker_type,
                    "price": 0,
                },
            )
            if created:
                self.stdout.write(self.style.WARNING(f"{ticker.name} created!"))

            date = parse_date(row["date"]).date()
            order = row["order"]
            quantity = int(row["quantity"])
            price = transform_to_decimal(row["price"])
            form = TransactionForm(
                data={
                    "wallet": wallet.id,
                    "ticker": ticker.id,
                    "date": date,
                    "price": price,
                    "quantity": quantity,
                    "order": order,
                }
            )
            if form.is_valid():
                instance = form.save(commit=False)
                objs.append(instance)
            else:
                self.stdout.write(self.style.ERROR(str(form.errors)))

        results = Transaction.objects.bulk_create(objs)

        message = f"{len(results)} transactions added."
        self.stdout.write(self.style.SUCCESS(message))
