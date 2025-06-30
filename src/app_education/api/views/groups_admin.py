from rest_framework import generics, permissions
from app_education.api.serializers.groups_admin import FacultyGroupsSerializer
from app_education.models import FacultyGroupsModel

from utils.permissions import (
    IsAuthenticatedPermission,
    IsSuperUserPermission,
    IsAdminUserPermission,
)
from utils.versioning import BaseVersioning
from utils.paginations import BasePagination


class AdminFacultyGroupsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    serializer_class = FacultyGroupsSerializer
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    search_fields = [
        "name",
        "faculty__fa_name",
        "faculty__en_name",
        "faculty__ar_name",
        "fields__fa_name",
        "fields__en_name",
        "fields__ar_name",
    ]
    filter_fields = [
        "faculty"
    ]
    queryset = FacultyGroupsModel.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [
                IsAuthenticatedPermission(),
                IsAdminUserPermission(),
                IsSuperUserPermission(),
            ]
        return [IsAuthenticatedPermission(), IsAdminUserPermission()]


class AdminFacultyGroupsUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    allowed_methods = ["OPTIONS", "PUT", "DELETE"]
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    serializer_class = FacultyGroupsSerializer
    versioning_class = BaseVersioning
    queryset = FacultyGroupsModel.objects.all()
    lookup_field = "pk"
