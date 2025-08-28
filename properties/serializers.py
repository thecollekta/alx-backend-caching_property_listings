from rest_framework import serializers

from properties.models import Property


class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer for the Property model
    """

    class Meta:
        model = Property
        fields = ["id", "title", "description", "price", "location", "created_at"]
        read_only_fields = ["id", "created_at"]
