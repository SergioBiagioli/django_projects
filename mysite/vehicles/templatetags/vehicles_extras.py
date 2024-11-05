from django import template

register = template.Library()

@register.filter
def get_field(obj, field_name):
    try:
        value = getattr(obj, field_name)
        if callable(value):
            return value()
        return value
    except AttributeError:
        return "N/A"
