from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organizers of a volunteer work to edit or delete it.
    """

    def has_permission(self, request, view):
        # Allow any authenticated user to view and create volunteer work
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the organizer of the volunteer work
        return obj.organizer == request.user
