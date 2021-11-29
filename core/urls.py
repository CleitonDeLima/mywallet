from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("to-buy/", views.stock_asset_to_buy, name="to-buy"),
]
