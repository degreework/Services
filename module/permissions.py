# -*- encoding: utf-8 -*-
from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    """
    Customized Permission
    """
    def has_permission(self, request, view):
        """check if user make request can create Module"""

        return "module.add_module" in request.user.get_all_permissions()
