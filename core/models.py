from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ticker(TimeStampedModel):
    class Types(models.IntegerChoices):
        ACAO = 0, _("Ação")
        FII = 1, _("FII")
        BDR = 2, _("BDR")
        ETF = 3, _("ETF")

    name = models.CharField(
        _("Nome"),
        max_length=10,
    )
    company_name = models.CharField(
        _("Nome da Empresa"),
        max_length=255,
    )
    document = models.CharField(
        _("CNPJ da Empresa"),
        max_length=14,
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
    name = models.CharField(_("Nome"), max_length=30, unique=True)

    class Meta:
        verbose_name = _("Carteira")
        verbose_name_plural = _("Carteiras")

    def __str__(self):
        return self.name

    def get_assets_url(self):
        return resolve_url("core:asset-list", self.id)


class WalletItem(TimeStampedModel):
    wallet = models.ForeignKey(
        "core.Wallet",
        verbose_name=_("Carteira"),
        on_delete=models.CASCADE,
        related_name="items",
    )
    ticker = models.ForeignKey(
        "core.Ticker",
        verbose_name=_("Papel"),
        on_delete=models.CASCADE,
    )
    started_in = models.DateField(
        verbose_name=_("Início"),
        blank=True,
        null=True,
    )
    closed_in = models.DateField(
        verbose_name=_("Encerrado"),
        blank=True,
        null=True,
    )
    allocation = models.DecimalField(
        verbose_name=_("Alocação"),
        max_digits=5,
        decimal_places=2,
    )
    entry_price = models.DecimalField(
        verbose_name=_("Preço de Entrada"),
        max_digits=15,
        decimal_places=2,
    )
    ceiling_price = models.DecimalField(
        verbose_name=_("Preço Teto"),
        max_digits=15,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _("Item da Carteira")
        verbose_name_plural = _("Itens da Carteira")


class Transaction(TimeStampedModel):
    class OrderTypes(models.TextChoices):
        BUY = "b", _("Compra")
        SELL = "s", _("Venda")

    wallet = models.ForeignKey(
        "core.Wallet",
        verbose_name=_("Carteira"),
        on_delete=models.SET_NULL,
        related_name="transactions",
    )
    ticker = models.ForeignKey(
        "core.Ticker",
        verbose_name=_("Papel"),
        on_delete=models.PROTECT,
    )
    date = models.DateField(_("Data da Negociação"))
    price = models.DecimalField(
        _("Valor Unitário"),
        max_digits=15,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField(_("Quantidade"))
    order = models.CharField(
        _("Ordem"),
        max_length=1,
        choices=OrderTypes.choices,
    )

    class Meta:
        verbose_name = _("Transação")
        verbose_name_plural = _("Transações")

    def __str__(self):
        return f"{self.get_order_display()} {self.quantity} {self.ticker}"
