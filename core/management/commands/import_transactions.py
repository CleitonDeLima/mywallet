import argparse
import csv
import logging
from decimal import Decimal

from dateutil.parser import parse as parse_date
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.forms import TransactionForm
from core.models import Ticker, Transaction, Wallet

logger = logging.getLogger(__name__)


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
            ticker_type = row["ticker_type"]
            ticker_name = row["ticker"]
            ticker, _ = Ticker.objects.get_or_create(
                name=ticker_name,
                defaults={
                    "type": ticker_type,
                    "price": 0,
                },
            )
            date = parse_date(row["date"]).date()
            order = row["order"]
            quantity = int(row["quantity"])
            price = Decimal(row["price"])
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
            instance = form.save(commit=False)
            objs.append(instance)

        results = Transaction.objects.bulk_create(objs)

        message = f"{len(results)} transactions added."
        self.stdout.write(self.style.SUCCESS(message))
