from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # 返回布尔, request 当前的请求,  view 应用在哪个视图上, obj是我们目前对象实例
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
