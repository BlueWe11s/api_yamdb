from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """
    Предоставляет права на осуществление запросов
    только c правами администратора
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_staff)
        )


class IsAdminorIsModerorIsSuperUser(permissions.BasePermission):
    """
    Представляет права доступа людям с админскими правами
    и модератерам.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_staff
                 or request.user.moderator)
        )
