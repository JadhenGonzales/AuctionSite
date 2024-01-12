from django import template
from django.template.defaultfilters import stringfilter

register=template.Library()

@register.filter
@stringfilter
def is_current(page, arg):
    return "active" if page == arg else ""