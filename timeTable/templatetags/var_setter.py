from django import template
register = template.Library()
@register.simple_tag
def set_var(val=None):
    return val
