from rest_framework import permissions
from .models import Quiz


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsOwnerOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.is_public:
                return True
        if request.user.is_authenticated:
            if obj.owner == request.user:
                return True

        return False

    def has_permission(self, request, view):
        return (
            Quiz.objects.filter(
                owner=request.user, id=request.resolver_match.kwargs["pk"]
            ).exists()
        )
