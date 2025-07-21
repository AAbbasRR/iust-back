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
                    "field": "fa_terms",
                    "fa_name": "قوانین فارسی ثبت نام",
                    "value": list_settings.fa_terms,
                },
                {
                    "id": 2,
                    "field": "en_terms",
                    "fa_name": "قوانین انگلیسی ثبت نام",
                    "value": list_settings.en_terms,
                },
                {
                    "id": 3,
                    "field": "ar_terms",
                    "fa_name": "قوانین عربی ثبت نام",
                    "value": list_settings.ar_terms,
                },
                {
                    "id": 11,
                    "field": "start_register_date",
                    "fa_name": "تاریخ شروع ثبت نام کارشناسی",
                    "value": str(list_settings.start_register_date),
                },
                {
                    "id": 12,
                    "field": "end_register_date",
                    "fa_name": "تاریخ اتمام ثبت نام کارشناسی",
                    "value": str(list_settings.end_register_date),
                },
                {
                    "id": 11,
                    "field": "start_phd_register_date",
                    "fa_name": "تاریخ شروع ثبت نام دکترا",
                    "value": str(list_settings.start_phd_register_date),
                },
                {
                    "id": 12,
                    "field": "end_phd_register_date",
                    "fa_name": "تاریخ اتمام ثبت نام دکترا",
                    "value": str(list_settings.end_phd_register_date),
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
