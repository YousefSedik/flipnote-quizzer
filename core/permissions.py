from rest_framework import permissions


class IsQuizOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if "pk" in view.kwargs:
            quiz_id = view.kwargs["pk"]
            from .models import Quiz

            try:
                quiz = Quiz.objects.get(pk=quiz_id)
                return quiz.owner == request.user
            except Quiz.DoesNotExist:
                return False

        return True


class IsQuestionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.quiz.owner == request.user

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if "pk" in view.kwargs:
            quiz_id = view.kwargs["pk"]
            from .models import Quiz

            try:
                quiz = Quiz.objects.get(pk=quiz_id)
                return quiz.owner == request.user
            except Quiz.DoesNotExist:
                return False

        return True


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
