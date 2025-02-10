from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value of a dictionary given a key."""
    return dictionary.get(key, "Not Available")
