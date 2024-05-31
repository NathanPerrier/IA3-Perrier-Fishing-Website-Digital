from django import template

register = template.Library()

@register.filter
def get_item(list, index):
    try:
        return list[index].common_name if index < len(list) else None
    except KeyError:
        return list[index].common_name if index < len(list) else None
    

@register.filter
def replace_spaces(value):
    return value.replace(' ', '_')


@register.filter
def clean_file(value):
    """
    This function removes the 'C:\\' prefix from the given file path.
    """
    return value.replace('C:\\', '')