import argparse
import csv
import logging
from decimal import Decimal

from dateutil.parser import parse as parse_date
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.forms import TransactionForm
from core.models import Ticker, Transaction, Wallet

User = get_user_model()
logger = logging.getLogger(__name__)


def transform_to_decimal(value) -> Decimal:
    digit_value = value.replace(",", "").replace(".", "")
    return Decimal(digit_value) / Decimal("100")


def get_ticker_type(value) -> int:
    value = value.lower()
    if value in ["fundos imobiliários", "fii"]:
        type = Ticker.Types.FII
    elif value in ["ações", "ação"]:
        type = Ticker.Types.ACAO
    elif value == "bdr":
        type = Ticker.Types.BDR
    elif value == "etf":
        type = Ticker.Types.ETF
    else:
        type = None

    return type


def get_order_type(value):
    value = value.lower()
    if value in ["c", "b", "compra", "buy"]:
        type = Transaction.OrderTypes.BUY
    elif value in ["v", "s", "venda", "sell"]:
        type = Transaction.OrderTypes.SELL
    else:
        type = None

    return type


class Command(BaseCommand):
    help = "Updates stock price via yahoo finances"

    def add_arguments(self, parser) -> None:
        parser.add_argument("file", type=argparse.FileType("r"))
        parser.add_argument("wallet_name")
        parser.add_argument("user_id")

    def handle(self, *args, **options):
        file = options["file"]
        wallet_name = options["wallet_name"]
        user_id = options["user_id"]

        user = User.objects.filter(id=user_id).first()
        if not user:
            self.stdout.write(
                self.style.ERROR(f"User with id {user_id} not found.")
            )
            return

        wallet, created = Wallet.objects.get_or_create(
            name=wallet_name, user=user
        )
        if created:
            self.stdout.write(f"Wallet {wallet_name} created.")

        fieldnames = [
            "date",
            "ticker_type",
            "ticker",
            "order",
            "quantity",
            "price",
        ]
        reader = csv.DictReader(file, fieldnames=fieldnames)
        transactions = []
        for row in reader:
            ticker_name = row["ticker"]
            ticker_type = get_ticker_type(row["ticker_type"])

            if ticker_type is None:
                continue

            ticker = self.create_ticker(ticker_name, ticker_type)

            date = parse_date(row["date"]).date()
            price = transform_to_decimal(row["price"])
            quantity = row["quantity"]
            order = get_order_type(row["order"])
            if order is None:
                continue

            transaction = self.create_transaction(
                wallet,
                ticker,
                date,
                price,
                quantity,
                order,
            )
            if transaction:
                transactions.append(transaction)

        results = Transaction.objects.bulk_create(transactions)
        message = f"{len(results)} transactions added."
        self.stdout.write(self.style.SUCCESS(message))

    def create_ticker(self, ticker_name, ticker_type):
        ticker, created = Ticker.objects.get_or_create(
            name=ticker_name.upper(),
            defaults={
                "type": ticker_type,
                "price": 0,
            },
        )
        if created:
            self.stdout.write(self.style.WARNING(f"{ticker.name} created!"))

        return ticker

    def create_transaction(self, wallet, ticker, date, price, quantity, order):
        form = TransactionForm(
            data={
                "ticker": ticker.id,
                "date": date,
                "price": price,
                "quantity": quantity,
                "order": order,
            }
        )
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.wallet = wallet
            return transaction

        self.stdout.write(self.style.ERROR(str(form.errors)))
