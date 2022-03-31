from django.urls import include, path

from core import views

app_name = "core"


transactions_urls = [
    path("", views.transaction_list, name="transaction-list"),
    path("new/", views.transaction_create, name="transaction-create"),
    path(
        "<int:pk>/update/",
        views.transaction_update,
        name="transaction-update",
    ),
    path(
        "<int:pk>/delete/",
        views.transaction_delete,
        name="transaction-delete",
    ),
    path(
        "all/delete/",
        views.transaction_delete_all,
        name="transaction-delete-all",
    ),
    path("tax/", views.income_tax, name="income-tax"),
    path("import/", views.transaction_import, name="transaction-import"),
]

urlpatterns = [
    path("", views.home, name="home"),
    path("account/", views.account_menu, name="account-menu"),
    path("transactions/", include(transactions_urls)),
]
