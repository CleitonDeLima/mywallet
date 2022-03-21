from django.contrib.auth.decorators import login_required
from django.db.models import Avg, DecimalField, ExpressionWrapper, F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import TransactionForm
from core.models import Transaction, Wallet


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def transaction_list(request):
    wallet = Wallet.objects.first()

    context = {
        "transaction_list": wallet.transactions.select_related("ticker"),
    }
    return render(request, "transactions/transaction_list.html", context)


@login_required
def transaction_create(request):
    form = TransactionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        transaction = form.save(commit=False)
        transaction.wallet = Wallet.objects.first()
        transaction.save()
        return redirect("core:transaction-list")

    context = {"form": form}
    return render(request, "transactions/transaction_form.html", context)


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    form = TransactionForm(request.POST or None, instance=transaction)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("core:transaction-list")

    context = {"form": form, "transaction": transaction}
    return render(request, "transactions/transaction_form.html", context)


@login_required
def income_tax(request):
    buy = Sum(
        "quantity",
        filter=Q(order=Transaction.OrderTypes.BUY),
        default=0,
    )
    sell = Sum(
        "quantity",
        filter=Q(order=Transaction.OrderTypes.SELL),
        default=0,
    )
    queryset = (
        Transaction.objects.values(
            "ticker__name",
            "ticker__company_name",
            "ticker__document",
        )
        .annotate(
            quantity=buy - sell,
            avg_price=Avg("price", filter=Q(order=Transaction.OrderTypes.BUY)),
            type=F("ticker__type"),
        )
        .filter(date__year__lte=2021)
        .order_by("type", "ticker__name")
    )
    context = {"record_list": queryset}
    return render(request, "transactions/income_tax.html", context)


@login_required
def wallet_asset(request, wallet_id):
    buy_filter = Q(order=Transaction.OrderTypes.BUY)
    sell_filter = Q(order=Transaction.OrderTypes.SELL)

    asset_list = (
        Transaction.objects.filter(wallet_id=wallet_id)
        .alias(
            buy_quantity=Sum("quantity", filter=buy_filter, default=0),
            sell_quantity=Sum("quantity", filter=sell_filter, default=0),
            ticker_total_price=F("price") * F("quantity"),
        )
        .values(
            "ticker__name",
            "ticker__price",
        )
        .annotate(
            avg_price=ExpressionWrapper(
                Sum("ticker_total_price", filter=buy_filter)
                / Sum("quantity", filter=buy_filter),
                output_field=DecimalField(),
            ),
            total_quantity=F("buy_quantity") - F("sell_quantity"),
            total_price=ExpressionWrapper(
                F("ticker__price") * F("total_quantity"),
                output_field=DecimalField(),
            ),
        )
        .filter(total_quantity__gt=0)
        .order_by("ticker__name")
    )
    context = {"asset_list": asset_list}
    return render(request, "wallet/asset_list.html", context)
