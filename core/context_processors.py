from django.conf import settings
from django.utils.translation import get_language

def google_maps_api_key(request):
    current_language = get_language() or settings.LANGUAGE_CODE
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'MAP_TRANSLATIONS': settings.MAP_TRANSLATIONS.get(current_language, settings.MAP_TRANSLATIONS['ar'])
    }