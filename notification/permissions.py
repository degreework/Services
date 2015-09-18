from rest_framework import permissions

class IsRecipient(permissions.BasePermission):
    """
    Only IsRecipient can do it
    """
    def has_object_permission(self, request, view, obj):
        return obj.recipient == request.user
