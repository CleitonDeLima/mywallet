from io import StringIO

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, DecimalField, ExpressionWrapper, F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import TransactionForm, TransactionImportForm
from core.management.commands.import_transactions import import_transactions
from core.models import Transaction


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def account_menu(request):
    return render(request, "account/menu.html")


@login_required
def transaction_list(request):
    wallet = request.user.wallets.first()

    context = {
        "transaction_list": wallet.transactions.select_related("ticker"),
        "title": "Transações",
    }
    return render(request, "transactions/transaction_list.html", context)


@login_required
def transaction_create(request):
    form = TransactionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        transaction = form.save(commit=False)
        transaction.wallet = request.user.wallets.first()
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
def transaction_delete(request, pk):
    transaction = get_object_or_404(
        Transaction, id=pk, wallet__user_id=request.user.id
    )

    if request.method == "POST":
        transaction.delete()
        return redirect("core:transaction-list")

    context = {"transaction": transaction}
    return render(
        request, "transactions/transaction_confirm_delete.html", context
    )


@login_required
def transaction_delete_all(request):
    queryset = Transaction.objects.filter(wallet__user_id=request.user.id)

    if request.method == "POST":
        queryset.delete()
        return redirect("core:transaction-list")

    total = queryset.count()
    context = {
        "message": (
            f"Tem certeza que deseja excluir as {total} transações? "
            "Isso não pode ser desfeito."
        ),
    }
    return render(
        request, "transactions/transaction_confirm_delete.html", context
    )


@login_required
def transaction_import(request):
    form = TransactionImportForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        wallet = request.user.wallets.first()
        file = form.cleaned_data["file"].read().decode("utf-8")
        import_transactions(StringIO(file), wallet)
        return redirect("core:transaction-list")

    context = {"form": form}
    return render(request, "transactions/transaction_import.html", context)


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
        .filter(wallet__user_id=request.user.id, date__year__lte=2021)
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
