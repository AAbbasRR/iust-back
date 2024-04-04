from rest_framework.permissions import (
    AllowAny as AllowAnyPermission,
    IsAuthenticated as IsAuthenticatedPermission,
    IsAdminUser as IsAdminUserPermission,
)
from rest_framework.permissions import BasePermission

from utils import BaseErrors


class IsSuperUserPermission(BasePermission):
    message = {"status": False, "message": BaseErrors.user_is_not_admin}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CanIssuanceLetterPermission(BasePermission):
    message = {
        "status": False,
        "message": BaseErrors.user_do_not_have_permission_for_application,
    }

    def has_permission(self, request, view):
        return bool(request.user.can_issuance_letter)
