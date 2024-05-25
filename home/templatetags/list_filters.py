from django import template

register = template.Library()

@register.filter
def get_item(list, index):
    try:
        return list[index]['acceptedcommonname'] if index < len(list) else None
    except KeyError:
        return list[index]['scientificname'] if index < len(list) else None