from rest_framework import generics
from rest_framework.response import Response

from app_admin.models import SettingsModel
from app_admin.api.serializers.settings import SettingsSerializer

from utils import BaseVersioning
from utils.paginations import BasePagination
from utils.permissions import AllowAnyPermission, IsAuthenticatedPermission, IsAdminUserPermission


class SettingsView(generics.ListAPIView):
    permission_classes = [AllowAnyPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    queryset = SettingsModel.objects.all()
    serializer_class = SettingsSerializer
