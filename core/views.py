from django.shortcuts import get_object_or_404, render

from core.models import StockAsset, Wallet
from core.services import get_assets_to_buy, get_total_stock_asset


def base_template(request):
    return "__main.html" if request.htmx else "__base.html"


def base_context(request, **context):
    context["base_template"] = base_template(request)
    return context


def home(request):
    return render(request, "home.html", base_context(request))


def wallet_list(request):
    context = base_context(request, wallet_list=Wallet.objects.all())
    return render(request, "wallet/wallet_list.html", context)


def wallet_create(request):
    return render(request, "wallet/wallet_form.html", base_context(request))


def asset_list(request, wallet_id=None):
    if wallet_id is None:
        queryset = StockAsset.objects.all()
    else:
        wallet = get_object_or_404(Wallet, id=wallet_id)
        queryset = wallet.assets.all()

    context = base_context(request, asset_list=queryset)
    return render(request, "asset/asset_list.html", context)


def wallet_rebalancing(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id)
    total = get_total_stock_asset(wallet)
    queryset = get_assets_to_buy(wallet, total)
    context = base_context(request, total=total, asset_list=queryset)
    return render(request, "wallet/rebalancing.html", context)
