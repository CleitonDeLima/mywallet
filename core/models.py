from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ticket(TimeStampedModel):
    name = models.CharField(
        _("Name"),
        max_length=10,
    )
    price = models.DecimalField(
        _("Value"),
        max_digits=15,
        decimal_places=2,
    )

    def __str__(self):
        return self.name


class StockAsset(TimeStampedModel):
    ticket = models.ForeignKey(
        Ticket,
        verbose_name=_("Ticket"),
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
    )
    expected_allocation = models.DecimalField(
        _("Expected Allocation"),
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _("Ativo")
        verbose_name_plural = _("Ativos")

    def __str__(self):
        return str(self.ticket)
