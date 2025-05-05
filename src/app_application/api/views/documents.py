from rest_framework import generics

from app_application.api.serializers.documents import DocumentsSerializer
from app_application.models import DocumentModel

from utils import BaseVersioning
from utils.permissions import IsAuthenticatedPermission


class DocumentsCreateView(generics.CreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = DocumentsSerializer


class DocumentsDetailUpdateView(generics.RetrieveUpdateAPIView):
    allowed_methods = ["OPTIONS", "GET", "PUT"]
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = DocumentsSerializer
    lookup_field = "pk"

    def get_queryset(self):
        if self.request.user.is_agent:
            applications = self.request.user.agent_applications.all()
            documents = DocumentModel.objects.filter(application__in=applications)
            return documents
        else:
            return self.request.user.user_documents.all()
