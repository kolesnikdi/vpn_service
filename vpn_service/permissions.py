from rest_framework import permissions, exceptions


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        else:
            return True


class IsOwnerOr404(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        else:
            raise exceptions.NotFound()
