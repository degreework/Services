# -*- encoding: utf-8 -*-
from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Customized Parmission
    """
    def has_object_permission(self, request, view, obj):
        """check if user make request is objects's author"""
        return obj.author.id == request.user.id