from rest_framework import generics

from app_user.api.serializers.agents_admin import AdminAgentsListSerializers
from app_application.api.serializers.application_admin import (
    AdminApplicationListSerializer,
)
from app_user.models import UserModel
from app_application.models import ApplicationModel

from utils.permissions import (
    IsAuthenticatedPermission,
    IsAdminUserPermission,
    IsSuperUserPermission,
)
from utils.versioning import BaseVersioning
from utils.paginations import BasePagination


class AdminAgentsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminAgentsListSerializers
    queryset = UserModel.objects.filter(is_agent=True)


class AdminAgentUpdateAPIView(generics.UpdateAPIView):
    allowed_methods = ["OPTIONS", "PUT"]
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminAgentsListSerializers
    queryset = UserModel.objects.filter(is_agent=True)
    lookup_field = "pk"


class AdminAgentListApplicationsAPIView(generics.ListAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminApplicationListSerializer
    filterset_fields = ["agent"]
    queryset = ApplicationModel.objects.filter()
