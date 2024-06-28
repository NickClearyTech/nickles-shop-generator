from django import template

register = template.Library()


@register.filter(name="rarity_char_to_string")
def rarity_char_to_string(value):
    match value:
        case "L":
            return "Legendary"
        case "U":
            return "Uncommon"
        case "R":
            return "Rare"
        case "V":
            return "Very Rare"
        case "A":
            return "Artifact"
        case "C":
            return "Common"


@register.filter(name="price_to_price_string")
def price_to_price_string(value):
    if 10 <= value <= 100:
        return f"{value/10} silver"
    elif 100 <= value <= 1000:
        return f"{value/100} gold"
    elif value == 0:
        return "No price"
    else:
        return f"{value} copper"
