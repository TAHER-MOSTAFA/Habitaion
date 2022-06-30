from rest_framework.viewsets import ModelViewSet, GenericViewSet
from habitation.ads.models import AD, Favourites
from .serializers import ADSerializer, FavouriteSerializerCreate
from .permissions import OwnAdOrReadOnly, OwnFavouriteOrReadOnly
from rest_framework import mixins
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Exists, OuterRef
from json import loads as js_loads

ADS_WITHIN = 10000 # 10 KM
class ADViewSet(ModelViewSet):


    def get_queryset(self):
        filters = dict()
        data = self.request.query_params
        
        qs =  AD.objects.filter(available=True).annotate(is_fav=Exists(Favourites.objects.filter(user=self.request.user, ad_id=OuterRef("id"))))

        if data.get("name"):
            filters['name__icontains'] = str(data['name'])
        if data.get("price_min"):
            filters['price__gte'] = int(data['price_min'])
        if data.get("price_max"):
            filters['price__lte'] = int(data['price_max'])
        if data.get("type") and data['type'] in AD.AD_TYPES:
            filters['type'] = data['type']
        if data.get("rooms"):
            filters['bed_rooms_no'] = int(data['rooms'])
        if data.get('location'):
            pt = Point(js_loads(data['location']))
            filters['location__distance_lte'] = (
                pt,
                data.get("within", ADS_WITHIN)
                )
            print(filters)
            return qs.filter(**filters).annotate(distance=Distance('location', pt)).order_by("distance")

        return qs.filter(**filters)

    permission_classes = [OwnAdOrReadOnly]

    serializer_class = ADSerializer
from rest_framework import status
from rest_framework.response import Response

class FavouriteView(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [OwnFavouriteOrReadOnly]
    
    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return FavouriteSerializerCreate
    #     else:
    #         return ADSerializer
    serializer_class = FavouriteSerializerCreate
    
    def get_queryset(self):
        # return AD.objects.prefetch_related('favourites_set').filter(favourites__user_id=self.request.user.id)
        return Favourites.objects.select_related('ad').filter(user=self.request.user).order_by('-created')