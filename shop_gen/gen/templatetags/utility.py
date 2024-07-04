from django import template

register = template.Library()


@register.filter(name="decodify")
def decodify(value):
    """
    Replaces _ with spaces
    Transforms to title case
    """
    return value.replace("_", " ").title()
