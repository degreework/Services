# -*- encoding: utf-8 -*-
from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Customized Permission
    """
    def has_object_permission(self, request, view, obj):
        """check if user make request is objects's author"""
        return obj.author.id == request.user.id


class CanCreate(permissions.BasePermission):
    """
    Customized Permission
    """
    def has_permission(self, request, view):
        """check if user has permissions"""        
        return "activitie.add_activitieparent" in request.user.get_all_permissions()


class CanCheck(permissions.BasePermission):
    """
    Customized Permission
    """
    def has_permission(self, request, view):
        """check if user has permissions"""
        return "activitie.can_check_activitie" in request.user.get_all_permissions()