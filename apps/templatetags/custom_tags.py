from decimal import Decimal

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


@register.filter('remove_nulls')
def remove_nulls(value):
    return str(value)[:-2]


@register.filter('custom_date')
def custom_date(value):
    months = {
        1: 'Yanvar',
        2: 'Fevral',
        3: 'Mart',
        4: 'Aprel',
        5: 'May',
        6: 'Iyun',
        7: 'Iyul',
        8: 'Avgust',
        9: 'Sentabr',
        10: 'Oktabr',
        11: 'Noyabr',
        12: 'Dekabr',
    }
    if value.minute:
        return f"{value.day} - {months.get(value.month, '')} - {value.month} - {value.year}  {value.hour}:{value.minute}"
    return f"{value.day} - {months.get(value.month, '')} - {value.month} - {value.year}"


@register.filter(is_safe=True)
def custom_intcomma(value):
    """
    Split the given number into groups of four digits from the left.
    For example, 1234412321342131 becomes '1234 4123 2134 2131'.
    """
    try:
        if not isinstance(value, (float, Decimal)):
            value = int(value)
    except (TypeError, ValueError):
        return value

    result = str(value)

    result_with_spaces = ' '.join([result[i:i + 4] for i in range(0, len(result), 4)])

    return result_with_spaces


@register.filter('has_operator')
def has_operator(value):
    if value == "Operator":
        return True
    return False
