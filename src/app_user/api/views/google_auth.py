from rest_framework import generics
from rest_framework.response import Response

from app_user.api.serializers.google_auth import UserRegisterLoginGoogleAuthSerializer

from utils import BaseVersioning
from utils.permissions import AllowAnyPermission


class UserRegisterLoginGoogleAuthView(generics.GenericAPIView):
    permission_classes = [
        AllowAnyPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = UserRegisterLoginGoogleAuthSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=self.request.data)
        ser.is_valid(raise_exception=True)
        return Response(ser.validated_data)
