from rest_framework import generics

from app_education.api.serializers.field_of_study_admini import (
    AdminFieldOfStudySerializer,
)
from app_education.models import FieldOfStudyModel

from utils import BaseVersioning
from utils.paginations import BasePagination
from utils.permissions import IsAuthenticatedPermission, IsSuperUserPermission


class AdminFieldOfStudyListCreateView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminFieldOfStudySerializer
    queryset = FieldOfStudyModel.objects.all()
    filter_fields = "faculty"


class AdminFieldOfStudyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    allowed_methods = ["OPTIONS", "PUT", "DELETE"]
    permission_classes = [IsAuthenticatedPermission, IsSuperUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminFieldOfStudySerializer
    queryset = FieldOfStudyModel.objects.all()
    lookup_field = "pk"
