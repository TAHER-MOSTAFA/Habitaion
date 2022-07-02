from django.db import router
from habitation.ads.api.views import ADViewSet, FavouriteView
from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import AdView, AddAdView, SearchView
from django.views.generic import TemplateView


router = SimpleRouter()
# router.
router.register('ads', ADViewSet, basename='AD')
router.register('favourite', FavouriteView, basename='Favourite')


app_name = "ads"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("ad/<id>/", AdView.as_view(), name='ad-details'),
    path("search/", SearchView.as_view(), name='search'),
    path("add/", AddAdView.as_view(), name='add-ad')
]
