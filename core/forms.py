from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from core.models import Transaction, Wallet, WalletItem


class WalletForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Salvar"))

    class Meta:
        model = Wallet
        fields = ["name"]


class WalletItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Salvar"))

    class Meta:
        model = WalletItem
        fields = [
            "ticker",
            "started_in",
            "allocation",
            "entry_price",
            "ceiling_price",
        ]


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Salvar"))

    class Meta:
        model = Transaction
        fields = ["wallet", "ticker", "date", "price", "quantity", "order"]
