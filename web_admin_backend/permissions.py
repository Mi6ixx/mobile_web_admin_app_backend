from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated or is a super_user
        return request.user.is_staff


class IsAdminUserOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated or is an admin user
        return request.user and (request.user.is_admin or request.user.is_staff)

