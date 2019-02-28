from rest_framework.permissions import BasePermission

class Checking(BasePermission):
    def has_object_permission(self, request,view, obj):
        if request.user.is_staff or request.user == obj.organizer:
            return True
        return False