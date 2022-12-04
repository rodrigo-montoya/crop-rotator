from django import template

import datetime

register = template.Library()

@register.filter(name='times')
def times(value):
    return range(1, value+1)

@register.filter(name='add_days')
def add_days(value, days):
    return value + datetime.timedelta(days=days)

@register.filter
def active(things, active=True):
    return things.filter(active=active)
