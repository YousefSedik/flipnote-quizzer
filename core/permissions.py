from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it or view if quiz is public.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.owner == request.user:
            return True
        if request.method in permissions.SAFE_METHODS:
            if obj.is_public:
                return True

        return False
