from django import template
register = template.Library()

@register.simple_tag
def set_var1(val1=None):
    return val1