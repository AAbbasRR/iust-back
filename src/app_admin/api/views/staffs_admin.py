from rest_framework import generics

from app_admin.api.serializers.staffs_admin import (
    AdminStaffsListCreateUpdateSerializer,
    UserSerializer,
)
from app_admin.models import AdminModel
from app_user.models import UserModel

from utils.permissions import IsAuthenticatedPermission, IsSuperUserPermission
from utils.paginations import BasePagination
from utils.versioning import BaseVersioning


class AdminStaffsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsSuperUserPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = UserSerializer
    search_fields = ["username", "sub", "email", "user_profile__first_name", "user_profile__last_name"]
    queryset = UserModel.objects.filter(
        is_staff=True, is_superuser=False
    ).prefetch_related("user_admin")


class AdminStaffsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsSuperUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminStaffsListCreateUpdateSerializer


class AdminStaffsUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    allowed_methods = ["OPTIONS", "PUT", "DELETE"]
    permission_classes = [IsAuthenticatedPermission, IsSuperUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminStaffsListCreateUpdateSerializer
    queryset = AdminModel.objects.all()
    lookup_field = "pk"
