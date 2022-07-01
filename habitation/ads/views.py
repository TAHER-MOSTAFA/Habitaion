from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, RedirectView
from habitation.ads.models import AD
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class AdView(TemplateView):
    template_name = "ads/units-details.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad'] = get_object_or_404(AD, id=self.kwargs['id'])
        return context
    