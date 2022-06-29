from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny 
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = None

    def get_object(self):
        assert isinstance(self.request.user.id, int)
        return self.queryset.get(id=self.request.user.id)

    @action(methods=['PATCH', 'GET'], detail=False)
    def me(self, request):
        if request.method == 'PATCH':
            return self.partial_update(request)
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

