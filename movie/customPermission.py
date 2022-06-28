from rest_framework.permissions import BasePermission

class PrivatePublicPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not obj.private:
            return True
        else:
            return obj.user == request.user

