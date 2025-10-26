"""
Template Filters for Currency and Date Formatting
فلاتر القوالب للعملة والتاريخ
"""
from django import template
from django.utils.safestring import mark_safe
from apps.core.models import SystemSettings

register = template.Library()


@register.filter(name='currency')
def currency(value):
    """
    تنسيق العملة - Format currency
    Usage: {{ amount|currency }}
    Output: $1,234.56
    """
    try:
        settings = SystemSettings.load()
        symbol = settings.currency_symbol
        amount = float(value)
        return mark_safe(f"{symbol}{amount:,.2f}")
    except (ValueError, TypeError):
        return value


@register.filter(name='currency_code')
def currency_code(value):
    """
    تنسيق العملة مع الكود - Format currency with code
    Usage: {{ amount|currency_code }}
    Output: $1,234.56 USD
    """
    try:
        settings = SystemSettings.load()
        symbol = settings.currency_symbol
        code = settings.currency
        amount = float(value)
        return mark_safe(f"{symbol}{amount:,.2f} {code}")
    except (ValueError, TypeError):
        return value


@register.simple_tag
def get_currency_symbol():
    """
    الحصول على رمز العملة - Get currency symbol
    Usage: {% get_currency_symbol %}
    Output: $
    """
    settings = SystemSettings.load()
    return settings.currency_symbol


@register.simple_tag
def get_currency_code():
    """
    الحصول على كود العملة - Get currency code
    Usage: {% get_currency_code %}
    Output: USD
    """
    settings = SystemSettings.load()
    return settings.currency

