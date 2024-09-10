# custom_filters.py
from django import template
from django.db.models import Q

register = template.Library()

@register.filter(name='filter_by_type_and_brand')
def filter_by_type_and_brand(products, product_brand):
    product_type, brand = product_brand.split(',')
    return products.filter(product_type=product_type, brand=brand).order_by('-positive_percentage')


@register.filter(name='replace_underscores_with_spaces')
def replace_underscores_with_spaces(value):
    return value.replace('_', ' ')
