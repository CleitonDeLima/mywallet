from allauth.account.signals import user_signed_up
from django.conf import settings
from django.db import models
from django.db.models import Case, F, When
from django.dispatch import receiver
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
    name = models.CharField(_("Nome"), max_length=30)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Usuário"),
        on_delete=models.CASCADE,
        related_name="wallets",
    )

    class Meta:
        verbose_name = _("Carteira")
        verbose_name_plural = _("Carteiras")

    def __str__(self):
        return self.name

    def get_assets_url(self):
        return resolve_url("core:asset-list", self.id)


class TransactionManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            total_price=Case(
                When(
                    order=Transaction.OrderTypes.SELL,
                    then=-F("price") * F("quantity"),
                ),
                default=F("price") * F("quantity"),
                output_field=models.DecimalField(),
            ),
        )
        return queryset


class Transaction(TimeStampedModel):
    class OrderTypes(models.TextChoices):
        BUY = "b", _("Compra")
        SELL = "s", _("Venda")

    wallet = models.ForeignKey(
        "core.Wallet",
        verbose_name=_("Carteira"),
        on_delete=models.CASCADE,
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

    objects = TransactionManager()

    class Meta:
        verbose_name = _("Transação")
        verbose_name_plural = _("Transações")

    def __str__(self):
        return f"{self.get_order_display()} {self.quantity} {self.ticker}"


@receiver(user_signed_up)
def create_user_wallet(request, user, **kwargs):
    Wallet.objects.create(name="Principal", user=user)
