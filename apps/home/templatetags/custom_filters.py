# custom_filters.py

from django import template

register = template.Library()

@register.filter(name="split_segments")
def split_segments(value, separator):
    return value.split(separator)

@register.filter(name='add_one')
def add_one(value):
    return value + 1
