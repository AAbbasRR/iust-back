from rest_framework import generics
from rest_framework.response import Response

from app_admin.models import SettingsModel
from app_admin.api.serializers.settings_admin import AdminSettingsSerializer

from utils import BaseVersioning
from utils.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class AdminSettingsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        list_settings = SettingsModel.objects.first()
        return Response(
            [
                {
                    "id": 1,
                    "field": "fa_signup_terms",
                    "fa_name": "قوانین فارسی قبل ثبت نام",
                    "value": list_settings.fa_signup_terms,
                },
                {
                    "id": 2,
                    "field": "en_signup_terms",
                    "fa_name": "قوانین انگلیسی قبل ثبت نام",
                    "value": list_settings.en_signup_terms,
                },
                {
                    "id": 3,
                    "field": "ar_signup_terms",
                    "fa_name": "قوانین عربی قبل ثبت نام",
                    "value": list_settings.ar_signup_terms,
                },
                {
                    "id": 4,
                    "field": "fa_before_sign_text",
                    "fa_name": "متن فارسی راهنما قبل از ورود یا ثبت نام",
                    "value": list_settings.fa_before_sign_text,
                },
                {
                    "id": 5,
                    "field": "en_before_sign_text",
                    "fa_name": "متن انگلیسی راهنما قبل از ورود یا ثبت نام",
                    "value": list_settings.en_before_sign_text,
                },
                {
                    "id": 6,
                    "field": "ar_before_sign_text",
                    "fa_name": "متن عربی راهنما قبل از ورود یا ثبت نام",
                    "value": list_settings.ar_before_sign_text,
                },
                {
                    "id": 7,
                    "field": "fa_before_new_application_text",
                    "fa_name": "متن فارسی راهنما قبل از ثبت اپلیکیشن جدید",
                    "value": list_settings.fa_before_new_application_text,
                },
                {
                    "id": 8,
                    "field": "en_before_new_application_text",
                    "fa_name": "متن انگلیسی راهنما قبل از ثبت اپلیکیشن جدید",
                    "value": list_settings.en_before_new_application_text,
                },
                {
                    "id": 9,
                    "field": "ar_before_new_application_text",
                    "fa_name": "متن عربی راهنما قبل از ثبت اپلیکیشن جدید",
                    "value": list_settings.ar_before_new_application_text,
                },
                {
                    "id": 10,
                    "field": "admin_application_text",
                    "fa_name": "متن راهنما جزییات پرونده در پنل ادمین",
                    "value": list_settings.admin_application_text,
                },
                {
                    "id": 11,
                    "field": "start_application_date",
                    "fa_name": "تاریخ شروع ثبت نام کاربران",
                    "value": str(list_settings.start_application_date),
                },
                {
                    "id": 12,
                    "field": "end_application_date",
                    "fa_name": "تاریخ اتمام ثبت نام کاربران",
                    "value": str(list_settings.end_application_date),
                },
            ]
        )


class AdminUpdateView(generics.UpdateAPIView):
    allowed_methods = ["OPTIONS", "PUT"]
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminSettingsSerializer

    def get_object(self):
        return SettingsModel.objects.first()
