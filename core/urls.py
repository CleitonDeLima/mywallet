from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "hx/stock-asset-to-buy/",
        views.stock_asset_to_buy,
        name="stock-asset-to-buy",
    ),
]
