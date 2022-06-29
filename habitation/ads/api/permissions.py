from rest_framework.permissions import BasePermission, SAFE_METHODS

class OwnAdOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.lord_id == request.user.id
class OwnFavouriteOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id
