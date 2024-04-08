from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        # # if we have a logged in user and the user is staff or if the request is Get
        # admin_permission = bool(request.user and request.user.is_staff)
        # return request.method == "GET" or admin_permission
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)


class ReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permission for read-only request
            return True
        else:
            # Check permissions for write request
            return obj.review_user == request.user
