from rest_framework.viewsets import ModelViewSet
from habitation.ads.models import AD
from .serializers import ADSerializer
from .permissions import OwnAdOrReadOnly


class ADViewSet(ModelViewSet):
    queryset = AD.objects.filter(available=True)
    permission_classes = [OwnAdOrReadOnly]
    serializer_class = ADSerializer
    