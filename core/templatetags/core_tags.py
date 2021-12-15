from contextlib import suppress

from django import template
from django.templatetags.l10n import localize
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

register = template.Library()


@register.inclusion_tag("templatetags/breadcrumb_url.html")
def breadcrumb_url(title, url=None):
    if url is not None:
        with suppress(NoReverseMatch):
            url = reverse(url)

    active = not bool(url)
    return {"title": title, "url": url, "active": active}


@register.filter
def show_money(value, prefix="R$"):
    localize_value = localize(value)
    return f"{prefix} {localize_value}"
