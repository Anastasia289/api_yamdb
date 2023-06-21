from rest_framework import permissions


class IsSuperUserIsAdminIsModerIsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view,):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_superuser)


class IsAdminOrStuffPermission(permissions.BasePermission):
    """
    Allows access to staff members or authenticated users with admin role.
    """

    def has_permission(self, request, view):
        # Check if the user is staff or authenticated with admin role
        return (
            request.user.is_staff
            or request.user.is_admin)
