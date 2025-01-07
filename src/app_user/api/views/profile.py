from rest_framework import generics

from app_user.api.serializers.profile import ProfileSerializer, ProfileInfoSerializer

from utils import BaseVersioning
from utils.permissions import IsAuthenticatedPermission


class ProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    allowed_methods = ["OPTIONS", "GET", "PUT"]
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.user_profile


class ProfileInfoDetailUpdateView(generics.RetrieveUpdateAPIView):
    allowed_methods = ["OPTIONS", "GET", "PUT"]
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ProfileInfoSerializer

    def get_object(self):
        return self.request.user.user_profile
