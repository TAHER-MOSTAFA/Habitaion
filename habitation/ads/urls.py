from django.db import router
from habitation.ads.api.views import ADViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
# router.
router.register('ads', ADViewSet, basename='AD')

app_name = "ads"

urlpatterns = [] + router.urls
