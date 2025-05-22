from rest_framework.permissions import BasePermission

class IsOwnerOrNonModeratorCreate(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method == 'POST':
            return not user.groups.filter(name='moderators').exists()
        return True

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id
