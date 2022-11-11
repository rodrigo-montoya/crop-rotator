from django import template

register = template.Library()

@register.filter(name='times')
def times(value):
    return range(1, value+1)
