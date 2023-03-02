from rest_framework import permissions, exceptions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


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


# class IsPostIdExists(permissions.BasePermission):
#     """
#     Permission that check if blog_id exist. If post(blog_id) exist returns True and if not Rises 404 exception.
#     Due to this permission we may not make such check in views.
#     """
#
#     def has_permission(self, request, view):
#         post = Post.objects.filter(id=view.kwargs['id'])
#         if not post:
#             raise exceptions.NotFound()
#         return True
