from django.contrib import admin

from core.models import StockAsset, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "updated_at"]
    search_fields = ["name"]


@admin.register(StockAsset)
class StockAssetAdmin(admin.ModelAdmin):
    list_display = ["ticket", "quantity", "expected_allocation"]
    autocomplete_fields = ["ticket"]
