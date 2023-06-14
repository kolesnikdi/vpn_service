from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import permissions, exceptions

from registration.djng_views import DjangoRegisterTryView


class IsOwnerOr404(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):   # check if owner exist
            if obj.owner == request.user:   # check if owner == user
                return True
            else:
                raise exceptions.NotFound()
        elif hasattr(obj, 'company'):   # add new check if no user in request
            if obj.company.owner == request.user:   # check if company.owner == user
                return True
            else:
                raise exceptions.NotFound()
        return True


class IsNotAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        else:
            return True


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


ALLOWED_METHODS = ('GET', 'OPTIONS', 'HEAD', 'DELETE')
REDIRECT_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')

class TwoFactorAuthenticationOrRedirect(permissions.BasePermission):
    # """
    # """
    def has_permission(self, request, view):
        if request.method in ALLOWED_METHODS:
            return True
        #     # raise exceptions.NotFound()
        if request.method in REDIRECT_METHODS:
            import webbrowser
            ss = webbrowser.open_new_tab('http://127.0.0.1:8000/registration/djangofunction')
            # reverse('djangofunction')
            # DjangoRegisterTryView().as_view()
            # yy = DjangoRegisterTryView()
            # redirect('company')
            # raise exceptions.NotFound()
            return True
        return True


"""Don't catche 'POST' """
    # def has_object_permission(self, request, view, obj):
    #     return True




