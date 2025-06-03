from rest_framework import generics, response

from app_education.api.serializers.faculty import (
    FacultySerializer,
    AllFacultySerializer,
)
from app_education.models import FacultyModel

from utils import BaseVersioning
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

        grouped = {"Master": [], "P.H.D": []}

        for degree in ["Master", "P.H.D"]:
            serializer = FacultySerializer(
                faculties,
                many=True,
                context={"degree": degree, "request": request},
            )
            grouped[degree] = serializer.data

        return response.Response(grouped)


class FacultyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    queryset = FacultyModel.objects.prefetch_related("fields_of_studies").all()
    serializer_class = AllFacultySerializer
