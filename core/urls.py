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
    path("tax/", views.income_tax, name="income-tax"),
    path("import/", views.transaction_import, name="transaction-import"),
]

urlpatterns = [
    path("", views.home, name="home"),
    path("transactions/", include(transactions_urls)),
]
