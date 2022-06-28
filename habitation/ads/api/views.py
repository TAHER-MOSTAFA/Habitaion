from rest_framework.viewsets import ModelViewSet
from habitation.ads.models import AD
from .serializers import ADSerializer
from .permissions import OwnAdOrReadOnly

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

ADS_WITHIN = 10000 # 10 KM
class ADViewSet(ModelViewSet):
    filter_fields = {"name", ""}
    def get_queryset(self):
        filters = dict()
        data = self.request.query_params
        
        qs =  AD.objects.filter(available=True)

        if data.get("name"):
            filters['name__contains'] = str(data['name'])
        if data.get("price_min"):
            filters['price__gte'] = int(data['price_min'])
        if data.get("price_max"):
            filters['price__lte'] = int(data['price_max'])
        if data.get("type") and data['type'] in AD.AD_TYPES:
            filters['type'] = data['type']
        if data.get("rooms"):
            filters['bed_rooms_no'] = int(data['rooms'])
        if data.get('location'):
            pt = Point(data['location'])
            filters['location__distance_lte'] = (
                pt,
                data.get("within", ADS_WITHIN)
                )
            print(filters)
            return qs.filter(**filters).annotate(distance=Distance('location', pt)).order_by("distance")

        return qs.filter(**filters)

    permission_classes = [OwnAdOrReadOnly]

    serializer_class = ADSerializer
    