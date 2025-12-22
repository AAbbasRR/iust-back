from rest_framework import generics

from app_user.models import UserModel
from app_user.api.serializers.users_admin import AdminUserListSerializer

from utils.permissions import (
    IsAuthenticatedPermission,
    IsAdminUserPermission,
    IsSuperUserPermission,
)
from utils.versioning import BaseVersioning
from utils.paginations import BasePagination


class AdminAllUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission, IsSuperUserPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminUserListSerializer
    search_fields = ["email", "user_profile__phone_number", "user_profile__first_name", "user_profile__last_name",
                     "user_profile__passport_number"]
    queryset = UserModel.objects.filter(is_agent=False, is_staff=False, is_admin=False)


class AdminConvertUserToAgentAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission, IsSuperUserPermission]
    versioning_class = BaseVersioning
    queryset = UserModel.objects.filter(is_agent=False, is_staff=False, is_admin=False)
    lookup_field = "pk"

    def post(self, request, *args, **kwargs):
        agent = self.get_object()
        agent.is_agent = True
        agent.save()
        return response.Response(status=status.HTTP_200_OK)
