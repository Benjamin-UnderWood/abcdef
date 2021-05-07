from rest_framework import permissions


class BlackListPermission(permissions.BasePermission):
    message = 'Jack已经被纳入黑名单了！'

    def has_permission(self, request, view):

        return not request.user.username == 'jack'


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.username == request.user.username

