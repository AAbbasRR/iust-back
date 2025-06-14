from rest_framework import generics

from app_education.api.serializers.faculty_admin import AdminFacultySerializer
from app_education.models import FacultyModel

from utils import BaseVersioning
from utils.paginations import BasePagination
from utils.permissions import IsAuthenticatedPermission, IsSuperUserPermission


class AdminFacultyListCreateView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminFacultySerializer
    search_fields = ["fa_name", "en_name", "ar_name"]
    queryset = FacultyModel.objects.all()


class AdminFacultyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    allowed_methods = ["OPTIONS", "PUT", "DELETE"]
    permission_classes = [IsAuthenticatedPermission, IsSuperUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminFacultySerializer
    queryset = FacultyModel.objects.all()
    lookup_field = "pk"
