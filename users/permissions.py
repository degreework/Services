from rest_framework import permissions

class IsSelf(permissions.BasePermission):
    """
    Only owner can do it
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
