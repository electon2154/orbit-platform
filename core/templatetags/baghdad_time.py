from django import template
from django.utils import timezone
import pytz
from datetime import datetime

register = template.Library()

@register.simple_tag
def baghdad_now():
    """
    Returns current time in Baghdad timezone
    """
    baghdad_tz = pytz.timezone('Asia/Baghdad')
    return timezone.now().astimezone(baghdad_tz)

@register.simple_tag
def baghdad_date():
    """
    Returns current date in Baghdad timezone (Arabic format)
    """
    baghdad_time = baghdad_now()
    return baghdad_time.strftime('%A، %d %B %Y')

@register.simple_tag
def baghdad_time():
    """
    Returns current time in Baghdad timezone (Arabic format)
    """
    baghdad_time = baghdad_now()
    return baghdad_time.strftime('%I:%M:%S %p')

@register.simple_tag
def baghdad_datetime():
    """
    Returns current datetime in Baghdad timezone (full Arabic format)
    """
    return f"{baghdad_date()} - {baghdad_time()}"

@register.filter
def to_baghdad_time(value):
    """
    Converts a datetime to Baghdad timezone
    """
    if not value:
        return value
    
    baghdad_tz = pytz.timezone('Asia/Baghdad')
    if timezone.is_aware(value):
        return value.astimezone(baghdad_tz)
    else:
        # Assume UTC if naive
        utc_time = pytz.UTC.localize(value)
        return utc_time.astimezone(baghdad_tz)

@register.filter
def format_baghdad_date(value):
    """
    Formats a datetime as Arabic date in Baghdad timezone
    """
    baghdad_time = to_baghdad_time(value)
    if not baghdad_time:
        return ''
    
    # Arabic month names
    arabic_months = {
        1: 'يناير', 2: 'فبراير', 3: 'مارس', 4: 'أبريل',
        5: 'مايو', 6: 'يونيو', 7: 'يوليو', 8: 'أغسطس',
        9: 'سبتمبر', 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر'
    }
    
    # Arabic day names
    arabic_days = {
        0: 'الإثنين', 1: 'الثلاثاء', 2: 'الأربعاء', 3: 'الخميس',
        4: 'الجمعة', 5: 'السبت', 6: 'الأحد'
    }
    
    day_name = arabic_days.get(baghdad_time.weekday(), '')
    month_name = arabic_months.get(baghdad_time.month, '')
    
    return f"{day_name}، {baghdad_time.day} {month_name} {baghdad_time.year}"

@register.filter
def format_baghdad_time(value):
    """
    Formats a datetime as Arabic time in Baghdad timezone
    """
    baghdad_time = to_baghdad_time(value)
    if not baghdad_time:
        return ''
    
    hour = baghdad_time.hour
    minute = baghdad_time.minute
    second = baghdad_time.second
    
    # Convert to 12-hour format
    if hour == 0:
        hour_12 = 12
        period = 'ص'
    elif hour < 12:
        hour_12 = hour
        period = 'ص'
    elif hour == 12:
        hour_12 = 12
        period = 'م'
    else:
        hour_12 = hour - 12
        period = 'م'
    
    return f"{hour_12:02d}:{minute:02d}:{second:02d} {period}"

@register.inclusion_tag('components/baghdad_datetime.html')
def baghdad_datetime_widget(show_seconds=True, compact=False):
    """
    Renders a Baghdad datetime widget
    """
    return {
        'show_seconds': show_seconds,
        'compact': compact,
        'current_time': baghdad_now()
    } 