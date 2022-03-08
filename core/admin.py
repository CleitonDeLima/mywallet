from django.contrib import admin

from core.models import Ticker, Transaction, Wallet, WalletItem


@admin.register(Ticker)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "type", "updated_at"]
    list_filter = ["type"]
    search_fields = ["name"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["ticker", "order", "quantity", "price"]
    autocomplete_fields = ["ticker"]
    list_filter = ["order", "wallet"]


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    ...


@admin.register(WalletItem)
class WalletItemAdmin(admin.ModelAdmin):
    ...
