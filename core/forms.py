from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.validators import FileExtensionValidator

from core.models import Transaction, Wallet
from flatpickr.forms import FlatPickrDateInput


class WalletForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Salvar"))

    class Meta:
        model = Wallet
        fields = ["name"]


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.include_media = False
        self.helper.add_input(Submit("submit", "Salvar"))

    class Meta:
        model = Transaction
        fields = ["ticker", "date", "price", "quantity", "order"]
        widgets = {"date": FlatPickrDateInput({"dateFormat": "d/m/Y"})}


class TransactionImportForm(forms.Form):
    file = forms.FileField(
        label="Arquivo de Transações",
        widget=forms.ClearableFileInput(attrs={"accept": ".csv"}),
        validators=[FileExtensionValidator(["csv"])],
        help_text=(
            "Cuidado para não escolher um arquivo já importado, "
            "pode duplicar suas transações."
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Importar registros"))
