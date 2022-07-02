from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, RedirectView
from habitation.ads.models import AD
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Favourites, AD
class AdView(TemplateView):
    template_name = "ads/units-details.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad'] = get_object_or_404(AD, id=self.kwargs['id'])
        return context

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Exists, OuterRef
from json import loads as js_loads


ADS_WITHIN = 10000 # 10 KM

class SearchView(TemplateView):
    template_name = "ads/units.html"
    
    def get_queryset(self):
        filters = dict()
        data = self.request.GET
        
        qs =  AD.objects.filter(available=True)

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
            return qs.filter(**filters).annotate(distance=Distance('location', pt)).order_by("distance")
        print(filters)

        return qs.filter(**filters)

    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads'] = self.get_queryset()
        return context
    
class AddAdView(TemplateView):
    template_name = "ads/add-unit.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context