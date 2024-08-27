from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_delivery_crew

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_manager and not request.user.is_delivery_crew

class ReadOnlyOrIsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_manager