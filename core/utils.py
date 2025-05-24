from django.utils import timezone
import pytz
from datetime import datetime

def get_baghdad_now():
    """
    Returns current time in Baghdad timezone
    """
    baghdad_tz = pytz.timezone('Asia/Baghdad')
    return timezone.now().astimezone(baghdad_tz)

def convert_to_baghdad_time(dt):
    """
    Converts a datetime object to Baghdad timezone
    """
    if not dt:
        return dt
    
    baghdad_tz = pytz.timezone('Asia/Baghdad')
    if timezone.is_aware(dt):
        return dt.astimezone(baghdad_tz)
    else:
        # Assume UTC if naive
        utc_time = pytz.UTC.localize(dt)
        return utc_time.astimezone(baghdad_tz)

def format_baghdad_datetime(dt, include_time=True, include_seconds=False):
    """
    Formats a datetime in Arabic format for Baghdad timezone
    """
    baghdad_time = convert_to_baghdad_time(dt)
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
    
    date_str = f"{day_name}، {baghdad_time.day} {month_name} {baghdad_time.year}"
    
    if include_time:
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
        
        if include_seconds:
            time_str = f"{hour_12:02d}:{minute:02d}:{second:02d} {period}"
        else:
            time_str = f"{hour_12:02d}:{minute:02d} {period}"
        
        return f"{date_str} - {time_str}"
    
    return date_str

class BaghdadTimestampMixin:
    """
    Mixin for models to automatically handle Baghdad timezone timestamps
    """
    
    def save(self, *args, **kwargs):
        # Set Baghdad time for created_at and updated_at
        now = get_baghdad_now()
        
        if hasattr(self, 'created_at') and not self.created_at:
            self.created_at = now
        
        if hasattr(self, 'updated_at'):
            self.updated_at = now
        
        super().save(*args, **kwargs)
    
    def get_created_at_baghdad(self):
        """Returns created_at in Baghdad timezone"""
        return convert_to_baghdad_time(self.created_at) if hasattr(self, 'created_at') else None
    
    def get_updated_at_baghdad(self):
        """Returns updated_at in Baghdad timezone"""
        return convert_to_baghdad_time(self.updated_at) if hasattr(self, 'updated_at') else None
    
    def get_formatted_created_at(self, include_time=True, include_seconds=False):
        """Returns formatted created_at in Arabic"""
        if hasattr(self, 'created_at') and self.created_at:
            return format_baghdad_datetime(self.created_at, include_time, include_seconds)
        return ''
    
    def get_formatted_updated_at(self, include_time=True, include_seconds=False):
        """Returns formatted updated_at in Arabic"""
        if hasattr(self, 'updated_at') and self.updated_at:
            return format_baghdad_datetime(self.updated_at, include_time, include_seconds)
        return ''

def add_baghdad_timestamp_to_form_data(form_data):
    """
    Adds Baghdad timestamp to form data for create/update operations
    """
    now = get_baghdad_now()
    
    if 'created_at' not in form_data:
        form_data['created_at'] = now
    
    form_data['updated_at'] = now
    
    return form_data 