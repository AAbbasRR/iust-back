from rest_framework import generics, response, status

from app_user.api.serializers.agents_admin import AdminAgentsListSerializers
from app_application.api.serializers.application_admin import (
    AdminApplicationListSerializer,
)
from app_user.models import UserModel
from app_application.models import ApplicationModel

from utils.permissions import (
    IsAuthenticatedPermission,
    IsAdminUserPermission,
    IsSuperUserPermission,
)
from utils.versioning import BaseVersioning
from utils.paginations import BasePagination


class AdminAgentsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminAgentsListSerializers
    queryset = UserModel.objects.filter(is_agent=True)


class AdminAgentUpdateAPIView(generics.UpdateAPIView):
    allowed_methods = ["OPTIONS", "PUT"]
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminAgentsListSerializers
    queryset = UserModel.objects.filter(is_agent=True)
    lookup_field = "pk"


class AdminAgentRejectAccountAPIView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    queryset = UserModel.objects.filter(is_agent=True)
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        agent = self.get_object()
        agent.send_email_to_user(
            subject="رد شدن حساب کارگزاری",
            content={
                "title": "message",
                "data": {
                    "title": f"درخواست حساب کارگزاری شما رد شده است.",
                    "description": f"با سلام کاربر گرامی، ایمیل شما در لیست ایمیل‌های کارگزاران رسمی سازمان امور دانشجویان نیست. شما میتوانید از این پس به عنوان کاربر حقوقی از خدمات سایت استفاده کنید.",
                },
            },
        )
        return response.Response(status=status.HTTP_200_OK)



class AdminAgentListApplicationsAPIView(generics.ListAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminApplicationListSerializer
    filterset_fields = ["agent"]
    queryset = ApplicationModel.objects.filter()
