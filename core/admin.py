from django.contrib import admin

from core.models import StockAsset, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "type", "updated_at"]
    list_filter = ["type"]
    search_fields = ["name"]


@admin.register(StockAsset)
class StockAssetAdmin(admin.ModelAdmin):
    list_display = ["ticket", "quantity", "expected_allocation"]
    autocomplete_fields = ["ticket"]
