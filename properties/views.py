from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .models import Property
from .serializers import PropertySerializer


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    List all properties with response cached for 15 minutes
    """
    if request.method == "GET":
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return JsonResponse({"properties": serializer.data}, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)
