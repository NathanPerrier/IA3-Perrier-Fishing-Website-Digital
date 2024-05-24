from django import template

register = template.Library()

@register.filter
def get_item(list, index):
    try:
        return list[index]['acceptedcommonname'] if index < len(list) else None
    except:
        return list[index] if index < len(list) else None