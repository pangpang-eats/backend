from rest_framework import permissions
from apps.user.models import User

class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, _, obj):
        user: User = request.user
        return obj.owner == user