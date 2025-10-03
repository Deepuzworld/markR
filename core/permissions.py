# permission classes to handle the different user roles.

from rest_framework import permissions

class IsInstitutionAdmin(permissions.BasePermission):
    """Allows access only to users in the 'Institution_Admin' group."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Institution_Admin').exists()

class IsDepartmentHead(permissions.BasePermission):
    """Allows access only to users in the 'Department_Head' group."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Department_Head').exists()

class IsStudent(permissions.BasePermission):
    """Allows access only to users in the 'Student' group."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Student').exists()