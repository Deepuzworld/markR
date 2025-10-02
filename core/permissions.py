from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    """Allows access only to users in the 'Students' group."""
    def has_permission(self, request, view):
        # We also check if the user is authenticated.
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Students').exists()

class IsStudyingInstitution(permissions.BasePermission):
    """Allows access only to users in the 'Studying_Institutions' group."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Studying_Institutions').exists()

class IsOtherInstitution(permissions.BasePermission):
    """Allows access only to users in the 'Other_Institutions' group."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Other_Institutions').exists()