from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminorIsModerorIsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
            )
        ):
            return True
        return (
            request.method in ('PUT', 'PATCH', 'DELETE')
            and obj.author == request.user
        )


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )
