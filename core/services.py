from decimal import Decimal

from django.db.models import IntegerField, QuerySet
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.db.models.functions import Cast

from core.models import StockAsset, Wallet


def get_total_stock_asset(wallet: Wallet) -> Decimal:
    return (
        StockAsset.objects.filter(wallet=wallet)
        .annotate(
            total=F("ticket__price") * F("quantity"),
        )
        .aggregate(Sum("total"))["total__sum"]
    )


def get_assets_to_buy(wallet: Wallet, total: Decimal) -> QuerySet[StockAsset]:
    to_buy = Cast(
        F("quantity") * F("expected_allocation") / F("allocated")
        - F("quantity"),
        output_field=IntegerField(),
    )
    queryset = (
        StockAsset.objects.filter(wallet=wallet)
        .select_related("ticket")
        .annotate(
            total_price=F("ticket__price") * F("quantity"),
            allocated=(F("total_price") * 100) / total,
            quantity_to_buy=to_buy,
            value_to_buy=F("quantity_to_buy") * F("ticket__price"),
        )
        .order_by("allocated")
    )

    return queryset
