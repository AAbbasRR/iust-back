from rest_framework import generics, response

from app_education.api.serializers.faculty import FacultySerializer
from app_education.models import FacultyModel

from utils import BaseVersioning
from utils.paginations import BasePagination
from utils.permissions import IsAuthenticatedPermission, IsAdminUserPermission

from collections import defaultdict


class FacultyListByDegreeView(generics.ListAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning

    def list(self, request, *args, **kwargs):
        faculties = FacultyModel.objects.prefetch_related("fields_of_studies").filter(
            is_active=True
        )
        serializer = FacultySerializer(faculties, many=True)

        grouped = defaultdict(list)
        for faculty_data in serializer.data:
            degree = faculty_data["degree"]
            grouped[degree].append(faculty_data)

        return response.Response(grouped)


class FacultyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    queryset = FacultyModel.objects.prefetch_related("fields_of_studies").filter(
        is_active=True
    )
    serializer_class = FacultySerializer
