from rest_framework import permissions

class IsAdminOrStaffUser(permissions.BasePermission):
    """
    Custom permission to allow only admin or staff users to create lodges.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has either is_admin or is_staff set to True
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_staff)

