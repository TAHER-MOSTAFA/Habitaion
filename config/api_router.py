from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from habitation.users.api.views import UserViewSet
from habitation.ads.urls import router as ads_router

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.registry.extend(ads_router.registry)


app_name = "api"
urlpatterns = router.urls
