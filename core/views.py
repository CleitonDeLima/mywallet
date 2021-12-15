from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import TransactionForm, WalletForm
from core.models import Transaction, Wallet
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
        form.save()
        return redirect("core:wallet-list")

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
