from django.contrib.auth.decorators import login_required
from django.db.models import DecimalField, ExpressionWrapper, F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import TransactionForm, WalletForm, WalletItemForm
from core.models import Transaction, Wallet, WalletItem
from core.services import get_assets_to_buy, get_total_stock_asset


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def wallet_list(request):
    context = {"wallet_list": Wallet.objects.all()}
    return render(request, "wallet/wallet_list.html", context)


@login_required
def wallet_create(request):
    form = WalletForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        wallet = form.save()
        return redirect("core:walletitem-list", wallet.id)

    context = {"form": form}
    return render(request, "wallet/wallet_form.html", context)


@login_required
def wallet_update(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id)
    form = WalletForm(request.POST or None, instance=wallet)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("core:wallet-list")

    context = {"form": form, "wallet": wallet}
    return render(request, "wallet/wallet_form.html", context)


@login_required
def wallet_item_list(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id)
    wallet_items = wallet.items.all()
    context = {"wallet": wallet, "wallet_items": wallet_items}
    return render(request, "wallet/wallet_item_list.html", context)


@login_required
def wallet_item_create(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id)
    form = WalletItemForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.wallet = wallet
        item.save()
        return redirect("core:walletitem-list", wallet.id)

    context = {"wallet": wallet, "form": form}
    return render(request, "wallet/wallet_item_form.html", context)


@login_required
def wallet_item_update(request, wallet_id, item_id):
    item = get_object_or_404(WalletItem, id=item_id, wallet_id=wallet_id)
    form = WalletItemForm(request.POST or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("core:walletitem-list", item.wallet_id)

    context = {"item": item, "wallet": item.wallet, "form": form}
    return render(request, "wallet/wallet_item_form.html", context)


@login_required
def wallet_rebalancing(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id)
    total = get_total_stock_asset(wallet)
    queryset = get_assets_to_buy(wallet, total)
    context = {"total": total, "asset_list": queryset}
    return render(request, "wallet/rebalancing.html", context)


@login_required
def transaction_list(request, wallet_id=None):
    if wallet_id:
        queryset = Transaction.objects.filter(wallet_id=wallet_id)
    else:
        queryset = Transaction.objects.all()

    context = {
        "transaction_list": queryset.select_related("ticker"),
        "wallet_list": Wallet.objects.all(),
        "wallet_id": wallet_id,
    }
    return render(request, "transactions/transaction_list.html", context)


@login_required
def transaction_create(request):
    form = TransactionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
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
