from django.contrib.gis import admin
from .models import AD

@admin.register(AD)
class PlaceAdmin(admin.OSMGeoAdmin):
    default_zoom = 15
    default_lon = 3493953
    default_lat = 3639058
    map_width = 800
    map_height = 800