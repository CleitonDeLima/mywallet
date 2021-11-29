from decimal import Decimal

from django.db.models import IntegerField, QuerySet
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.db.models.functions import Cast

from core.models import StockAsset


def get_total_stock_asset() -> Decimal:
    return StockAsset.objects.annotate(
        total=F("ticket__price") * F("quantity"),
    ).aggregate(Sum("total"))["total__sum"]


def get_stock_asset_to_buy(total: Decimal) -> QuerySet[StockAsset]:
    queryset = (
        StockAsset.objects.select_related("ticket")
        .annotate(
            total_price=F("ticket__price") * F("quantity"),
            allocated=(F("total_price") * 100) / total,
            to_buy=(
                Cast(
                    F("quantity") * F("expected_allocation") / F("allocated")
                    - F("quantity"),
                    output_field=IntegerField(),
                )
            ),
        )
        .order_by("allocated")
    )

    return queryset
