from django import template

register = template.Library()

@register.filter
def cart_total(cart):
    if not cart:
        return 0
    return sum(item['quantity'] for item in cart.values()) 