from django import template
from django.templatetags.l10n import localize

register = template.Library()


@register.inclusion_tag("templatetags/breadcrumb.html")
def breadcrumb(**urls):
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    urls: dict
        The keys are the title and the value the url name.
    """
    return {"urls": urls}


@register.filter
def show_money(value, prefix="R$"):
    localize_value = localize(value)
    return f"{prefix} {localize_value}"
