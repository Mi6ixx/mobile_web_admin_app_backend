from rest_framework import permissions

class IsOwnerOfStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only methods for everyone
            return True
        # Check if the user making the request is the owner of the student object
        return obj.user == request.user
