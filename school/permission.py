from rest_framework import permissions


class UserPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False
