from django import template

register = template.Library()

def humandate(value):
    return value
