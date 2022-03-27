from rest_framework import permissions


class AuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_authenticated
            and request.user.is_moderator_or_admin
        )


class UserOrStaffOrReadOnly(permissions.BasePermission):
    """
    Анон имеет право только на чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_moderator_or_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method == "GET"
            or obj.username == request.user.username
            or request.user.is_moderator_or_admin
        )


class UserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
