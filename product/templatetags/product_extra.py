from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag(name='multiplication')
def multiplication(value, arg):
    return value * arg

