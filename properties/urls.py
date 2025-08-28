from django.urls import path

from properties.views import property_list

app_name = "properties"

urlpatterns = [
    path("", property_list, name="property-list"),
]
