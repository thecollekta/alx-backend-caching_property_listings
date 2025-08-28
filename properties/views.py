from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from properties.models import Property
from properties.serializers import PropertySerializer


@api_view(["GET"])
@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    List all properties with response cached for 15 minutes
    """
    properties = Property.objects.all()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
