from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ticket(TimeStampedModel):
    class Types(models.IntegerChoices):
        ACAO = 0, _("Ação")
        FII = 1, _("FII")
        BDR = 2, _("BDR")
        ETF = 3, _("ETF")

    name = models.CharField(
        _("Nome"),
        max_length=10,
    )
    price = models.DecimalField(
        _("Valor"),
        max_digits=15,
        decimal_places=2,
    )
    type = models.PositiveSmallIntegerField(
        _("Tipo"),
        choices=Types.choices,
    )

    class Meta:
        verbose_name = _("Papel")
        verbose_name_plural = _("Papeis")

    def __str__(self):
        return self.name


class Wallet(TimeStampedModel):
    name = models.CharField(_("Nome"), max_length=30)

    class Meta:
        verbose_name = _("Carteira")
        verbose_name_plural = _("Carteiras")

    def __str__(self):
        return self.name


class StockAsset(TimeStampedModel):
    ticket = models.ForeignKey(
        "core.Ticket",
        verbose_name=_("Papel"),
        on_delete=models.PROTECT,
    )
    wallet = models.ForeignKey(
        "core.Wallet",
        verbose_name=_("Carteira"),
        on_delete=models.SET_NULL,
        related_name="assets",
        null=True,
    )
    quantity = models.PositiveIntegerField(_("Quantidade"))
    expected_allocation = models.DecimalField(
        _("Alocação Esperada"),
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _("Ativo")
        verbose_name_plural = _("Ativos")

    def __str__(self):
        return f"{self.quantity} {self.ticket}"
