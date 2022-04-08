import json

from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import get_language

from flatpickr.i18n import get_flatpickr_locale

version = "4.6.11"


class FlatPickrDateInput(forms.DateInput):
    css_class_name = "flatpickr-input"

    def __init__(self, flatpickr_opts=None, attrs=None, format=None):
        super().__init__(attrs, format)
        if flatpickr_opts is None:
            flatpickr_opts = {}
        self.flatpickr_opts = flatpickr_opts
        self.i18n_name = get_flatpickr_locale(get_language())

        if "locale" not in flatpickr_opts:
            flatpickr_opts.update({"locale": self.i18n_name})

    @property
    def media(self):
        css = f"https://cdnjs.cloudflare.com/ajax/libs/flatpickr/{version}/flatpickr.min.css"
        js = f"https://cdnjs.cloudflare.com/ajax/libs/flatpickr/{version}/flatpickr.min.js"
        l10n_js = f"https://cdnjs.cloudflare.com/ajax/libs/flatpickr/{version}/l10n/{self.i18n_name}.min.js"
        init_js = "flatpickr/init.js"
        return forms.Media(
            css={"all": [css]},
            js=[js, l10n_js, init_js],
        )

    def build_attrs(self, base_attrs, extra_attrs=None):
        json_str = json.dumps(self.flatpickr_opts, cls=DjangoJSONEncoder)
        default_attrs = {"data-flatpickr-options": json_str}
        default_attrs.update(base_attrs)
        attrs = super().build_attrs(default_attrs, extra_attrs=extra_attrs)

        if "class" in attrs:
            attrs["class"] += " " + self.css_class_name
        else:
            attrs["class"] = self.css_class_name
        return attrs
