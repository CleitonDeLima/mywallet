from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("wallets/", views.wallet_list, name="wallet-list"),
    path("wallets/create/", views.wallet_create, name="wallet-create"),
    path(
        "wallets/<int:wallet_id>/to-buy/",
        views.wallet_rebalancing,
        name="rebalancing",
    ),
    path("assets/", views.asset_list, name="asset-list"),
    path("assets/<int:wallet_id>/", views.asset_list, name="asset-list"),
]
