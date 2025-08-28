from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from properties.serializers import PropertySerializer
from properties.utils import get_all_properties


@cache_page(60 * 15)  # Cache the entire view response for 15 minutes
def property_list(request):
    """
    List all properties with response cached for 15 minutes
    Uses get_all_properties() which caches the queryset for 1 hour
    """
    if request.method == "GET":
        properties = get_all_properties()  # Uses low-level caching
        serializer = PropertySerializer(properties, many=True)
        return JsonResponse({"properties": serializer.data}, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)
