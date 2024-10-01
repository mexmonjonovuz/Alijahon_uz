from django.template import Library

register = Library()


@register.filter('has_active_category')
def has_active_category(path, category_slug=None) -> str:
    if category_slug is None:
        return path.split('category/')[-1].strip('/') is None
    return path.split('category/')[-1].strip('/') == category_slug  # noqa


@register.filter()
def is_liked(user, product) -> bool:
    if user.is_anonymous:
        return False
    return user.likes.filter(product=product).exists()


@register.filter(name='length_is')
def length_is(value, length):
    """
    This filter checks if the length of the value (list, string, etc.) equals the specified length.

    Usage: {{ your_list|length_is:5 }} will return True if the list length is 5.
    """
    try:
        return len(value) == int(length)
    except (TypeError, ValueError):
        return False


@register.filter('spliter')
def split_path(path) -> str:
    return path.split('/')[-2]


@register.filter('distinct')
def distinct(value) -> set:
    category_list = set()
    if value not in category_list:
        category_list.add(value)
        return category_list
    return set()
