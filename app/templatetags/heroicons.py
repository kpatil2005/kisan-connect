from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def heroicon(name, style='outline', css_class=''):
    """Use Font Awesome icons instead of heroicons"""
    icons = {
        'shopping-cart': 'fa-solid fa-cart-shopping',
        'user': 'fa-solid fa-user',
        'home': 'fa-solid fa-house',
        'phone': 'fa-solid fa-phone',
        'login': 'fa-solid fa-right-to-bracket',
        'logout': 'fa-solid fa-right-from-bracket',
        'user-plus': 'fa-solid fa-user-plus',
    }
    fa_class = icons.get(name, 'fa-solid fa-circle-info')
    return mark_safe(f'<i class="{fa_class} {css_class}"></i>')
