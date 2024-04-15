
from rest_framework import permissions

class CanCreateProjectPermission(permissions.BasePermission):
    def has_permission(self, request , view):
        user_type = getattr(request.user, 'userType', None)
        return user_type in ['Admin', 'Project-Manager', 'Team-Leader']


# this will show how has the permission to allocate the task to emp
class Canallocateproject(permissions.BasePermission):
    def has_permission(self, request, view):
        user_type = getattr(request.user, 'userType', None)
        return user_type in [ 'Project-Manager']
    

