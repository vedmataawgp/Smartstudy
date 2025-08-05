from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if dictionary and key:
        return dictionary.get(key)
    return None

@register.filter
def sub(value, arg):
    """Subtract arg from value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def mul(value, arg):
    """Multiply value by arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide value by arg"""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def filter_by_status(queryset, status):
    """Filter queryset by status"""
    if queryset and status:
        return queryset.filter(status=status)
    return queryset

@register.filter
def avg_score(attempts):
    """Calculate average score from quiz attempts"""
    if not attempts:
        return 0
    total = sum(attempt.percentage for attempt in attempts)
    return total / len(attempts)

@register.filter
def best_score(attempts):
    """Get best score from quiz attempts"""
    if not attempts:
        return 0
    return max(attempt.percentage for attempt in attempts)

@register.filter
def avg_time(attempts):
    """Calculate average time from quiz attempts"""
    if not attempts:
        return 0
    valid_times = [attempt.time_taken for attempt in attempts if attempt.time_taken]
    if not valid_times:
        return 0
    return sum(valid_times) / len(valid_times)

@register.filter
def truncatechars(value, length):
    """Truncate string to specified length"""
    if len(str(value)) > length:
        return str(value)[:length] + '...'
    return str(value)

@register.filter
def pluralize(value, suffix='s'):
    """Add plural suffix if value is not 1"""
    try:
        if int(value) == 1:
            return ''
        return suffix
    except (ValueError, TypeError):
        return suffix