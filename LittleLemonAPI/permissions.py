from rest_framework import permissions
from django.contrib.auth.models import User, Group

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if(request.method == 'GET'):
            return True
        else:
            if User.objects.filter(pk=request.user.id, groups__name='Managers').exists():
                 return True

class IsDelivey(permissions.BasePermission):
    edit_methods = ("GET", "PUT", "PATCH")
    def has_permission(self, request, view):
        if User.objects.filter(pk=request.user.id, groups__name='Deliver_Crew').exists():
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False