from django import template

register = template.Library()


@register.filter()
def inclusiveList(number, start):
    return range(start, number + 1)


@register.filter()
def exclusiveList(number, start):
    return range(start, number)
