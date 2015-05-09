from django import template
import django.utils.timezone as tz

register = template.Library()

def humandate(value):
    date = value.date()
    today = tz.now().date()
    if date == today:
        return 'Today'
    else:
        return str(date)
