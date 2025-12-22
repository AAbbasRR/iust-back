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
from utils.classes import ManageMailService


class AdminAgentsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminAgentsListSerializers
    search_fields = ["email"]
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
        agent_email = ManageMailService(agent.email)
        agent_email.send_email_to_user(
            subject="رد شدن حساب کارگزاری",
            content={
                "title": "message",
                "data": {
                    "title": f"درخواست حساب کارگزاری شما رد شده است.",
                    "description": f"با سلام کاربر گرامی، ایمیل شما در لیست ایمیل‌های کارگزاران رسمی سازمان امور دانشجویان نیست. شما.",
                },
            },
        )
        agent.is_agent = False
        agent.is_locked = False
        agent.save()
        return response.Response(status=status.HTTP_200_OK)


class AdminAgentAcceptAccountAPIView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    queryset = UserModel.objects.filter(is_agent=True)
    lookup_field = "pk"

    def post(self, request, *args, **kwargs):
        agent = self.get_object()
        agent_email = ManageMailService(agent.email)
        agent_email.send_email_to_user(
            subject="تایید شدن حساب کارگزاری",
            content={
                "title": "message",
                "data": {
                    "title": f"درخواست حساب کارگزاری شما رد شده است.",
                    "description": f"کارگزار محترم حساب شما با موفقیت تایید شد. \n شما می‌توانید با استفاده از لینک زیر و وارد کردن اطلاعات حساب کاربری خود ثبت درخواست دانشجویان را وارد کرده و پیگیری نمایید.\n apply.iust.ac.ir/login\n با تشکر\nدفتر پردیس دانشجویان بین الملل دانشگاه علم و صنعت ایران ",
                },
            },
        )
        agent.is_locked = False
        agent.set_last_login()
        agent.save()
        return response.Response(status=status.HTTP_200_OK)


class AdminConvertAgentToUserAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission,IsSuperUserPermission]
    versioning_class = BaseVersioning
    queryset = UserModel.objects.filter(is_agent=True)
    lookup_field = "pk"

    def post(self, request, *args, **kwargs):
        agent = self.get_object()
        agent = agent.is_agent = False
        agent.save()
        return response.Response(status=status.HTTP_200_OK)