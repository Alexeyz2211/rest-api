from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # obj here is a UserProfile instance
        return obj.user == request.user
