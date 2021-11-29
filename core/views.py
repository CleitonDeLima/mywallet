from django.shortcuts import render

from core.services import get_stock_asset_to_buy, get_total_stock_asset


def home(request):
    return render(request, "home.html")


def stock_asset_to_buy(request):
    total = get_total_stock_asset()
    queryset = get_stock_asset_to_buy(total)
    context = {"total": total, "asset_list": queryset}
    return render(request, "_stock_asset_to_buy_table.html", context)
