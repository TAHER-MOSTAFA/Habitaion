from django.contrib.gis import admin
from .models import AD, Image, Spec


class StackedSpecsAdmin(admin.TabularInline):
    model = Spec
    fields = ("label", "value", "ad")
    readonly_fields = ("ad",)

    extra = 1

class StackedImageAdmin(admin.TabularInline):
    model = Image
    fields = ("image", "ad")
    readonly_fields = ("ad",)
    extra = 1

    def has_add_permission(self, request, *args, **kwargs):
        return True
@admin.register(AD)
class PlaceAdmin(admin.OSMGeoAdmin):
    default_zoom = 15
    default_lon = 3493953
    default_lat = 3639058
    map_width = 800
    map_height = 800
    
    inlines = (StackedSpecsAdmin, StackedImageAdmin)