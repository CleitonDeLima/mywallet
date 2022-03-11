from django.urls import include, path

from core import views

app_name = "core"

wallets_urls = [
    path("", views.wallet_list, name="wallet-list"),
    path("create/", views.wallet_create, name="wallet-create"),
    path("<int:wallet_id>/update/", views.wallet_update, name="wallet-update"),
    path(
        "<int:wallet_id>/items/",
        views.wallet_item_list,
        name="walletitem-list",
    ),
    path(
        "<int:wallet_id>/items/create/",
        views.wallet_item_create,
        name="walletitem-create",
    ),
    path(
        "<int:wallet_id>/items/<int:item_id>/update/",
        views.wallet_item_update,
        name="walletitem-update",
    ),
]

transactions_urls = [
    path("", views.transaction_list, name="transaction-list"),
    path("<int:wallet_id>/", views.transaction_list, name="transaction-list"),
    path("new/", views.transaction_create, name="transaction-create"),
    path(
        "<int:pk>/update/",
        views.transaction_update,
        name="transaction-update",
    ),
    path("tax/", views.income_tax, name="income_tax"),
]

urlpatterns = [
    path("", views.home, name="home"),
    path("wallets/", include(wallets_urls)),
    path("transactions/", include(transactions_urls)),
]
