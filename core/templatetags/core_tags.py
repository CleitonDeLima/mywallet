from django import template
from django.shortcuts import resolve_url
from django.template.defaultfilters import floatformat
from django.templatetags.l10n import localize
from django.urls.exceptions import NoReverseMatch

register = template.Library()


@register.inclusion_tag("templatetags/breadcrumb_url.html")
def breadcrumb_url(title, url=None, *args):
    if url is not None:
        try:
            url = resolve_url(url, *args)
        except NoReverseMatch:
            url = None

    active = not bool(url)
    return {"title": title, "url": url, "active": active}


@register.filter
def show_money(value, prefix="R$"):
    value = floatformat(value, 2)
    localize_value = localize(value)
    return f"{prefix} {localize_value}"
