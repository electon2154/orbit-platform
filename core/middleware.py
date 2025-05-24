from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
import pytz

class BaghdadTimezoneMiddleware(MiddlewareMixin):
    """
    Middleware to automatically activate Baghdad timezone for all requests
    and provide Baghdad time context to templates
    """
    
    def process_request(self, request):
        # Activate Baghdad timezone for this request
        baghdad_tz = pytz.timezone('Asia/Baghdad')
        timezone.activate(baghdad_tz)
        
        # Add Baghdad time to request context
        request.baghdad_time = timezone.now()
        
    def process_response(self, request, response):
        # Deactivate timezone after request
        timezone.deactivate()
        return response

class TimestampMiddleware(MiddlewareMixin):
    """
    Middleware to automatically add timestamp information to forms and models
    """
    
    def process_request(self, request):
        # Add current Baghdad time to request for use in forms
        if request.method in ['POST', 'PUT', 'PATCH']:
            baghdad_tz = pytz.timezone('Asia/Baghdad')
            current_time = timezone.now().astimezone(baghdad_tz)
            
            # Add timestamp to request META for access in forms/views
            request.META['BAGHDAD_TIMESTAMP'] = current_time.isoformat()
            request.META['BAGHDAD_TIMESTAMP_RAW'] = current_time
            
            # If it's a form submission, add created_at/updated_at if not present
            if hasattr(request, 'POST') and request.POST:
                # Create a mutable copy of POST data
                post_data = request.POST.copy()
                
                # Add timestamp fields if they don't exist
                if 'created_at' not in post_data:
                    post_data['created_at'] = current_time.isoformat()
                if 'updated_at' not in post_data:
                    post_data['updated_at'] = current_time.isoformat()
                
                # Replace the POST data
                request.POST = post_data 