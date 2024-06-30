from django import template
import math

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
        return f"{int(math.floor(value/10))} silver"
    elif 100 <= value:
        return f"{int(math.floor(value/100))} gold"
    elif value == 0:
        return "No price"
    else:
        return f"{int(value)} copper"


@register.filter(name="spell_level_int_to_string")
def spell_level_int_to_string(value):
    match value:
        case 0:
            return "Cantrip"
        case 1:
            return "1st Level"
        case 2:
            return "2nd Level"
        case 3:
            return "3rd Level"
        case 4:
            return "4th Level"
        case 5:
            return "5th Level"
        case 6:
            return "6th Level"
        case 7:
            return "7th Level"
        case 8:
            return "8th Level"
        case 9:
            return "9th Level"
