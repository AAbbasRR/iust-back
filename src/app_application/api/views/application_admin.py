from django.http import HttpResponse
from django.db.models import OuterRef, Subquery, FloatField

from rest_framework import generics, response

from app_application.models import ApplicationModel
from app_application.api.serializers.application_admin import (
    AdminApplicationListSerializer,
    AdminApplicationExportResource,
    AdminDetailApplicationSerializer,
    AdminUpdateApplicationSerializer,
    AdminSubmitApplicationLetterSerializer,
)
from app_application.filters.applications import ApplicationListFilter
from app_education.models import BachelorDegreeModel, MasterDegreeModel
from app_admin.models import AdminModel

from utils.permissions import (
    IsAuthenticatedPermission,
    IsAdminUserPermission,
    IsSuperUserPermission,
    CanIssuanceLetterPermission,
)
from utils.versioning import BaseVersioning
from utils.paginations import BasePagination


class AdminAllApplicationView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminApplicationListSerializer
    ordering_fields = ["create_at", "bachelor_gpa", "master_gpa"]
    filterset_class = ApplicationListFilter

    def get_queryset(self):
        bachelor_gpa_subquery = BachelorDegreeModel.objects.filter(
            user=OuterRef("user_id")
        ).values("gpa")[:1]

        master_gpa_subquery = MasterDegreeModel.objects.filter(
            user=OuterRef("user_id")
        ).values("gpa")[:1]

        queryset = ApplicationModel.objects.annotate(
            bachelor_gpa=Subquery(bachelor_gpa_subquery, output_field=FloatField()),
            master_gpa=Subquery(master_gpa_subquery, output_field=FloatField()),
        )

        if self.request.user.is_superuser or self.request.user.is_admin:
            return queryset.exclude(
                status=ApplicationModel.ApplicationStatusOptions.Not_Completed
            ).distinct()
        else:
            return (
                queryset.filter(
                    application_referral__destination_user=self.request.user
                )
                .exclude(status=ApplicationModel.ApplicationStatusOptions.Not_Completed)
                .distinct()
            )


class AdminExportApplicationListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    ordering_fields = ["create_at"]
    filterset_class = ApplicationListFilter

    def get_queryset(self):
        if self.request.user.is_superuser is True or self.request.user.is_admin is True:
            return ApplicationModel.objects.all().exclude(
                status=ApplicationModel.ApplicationStatusOptions.Not_Completed
            )
        else:
            return ApplicationModel.objects.filter(
                application_referral__destination_user=self.request.user
            ).exclude(status=ApplicationModel.ApplicationStatusOptions.Not_Completed)

    def get(self, *args, **kwargs):
        resource_class = AdminApplicationExportResource(user=self.request.user)
        dataset = resource_class.export(self.get_queryset())

        response = HttpResponse(dataset.xlsx, content_type="text/xlsx")
        response["Content-Disposition"] = 'attachment; filename="export_orders.xlsx"'
        return response


class AdminReferralApplicationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminApplicationListSerializer
    ordering_fields = ["create_at"]
    filterset_class = ApplicationListFilter

    def get_queryset(self):
        return ApplicationModel.objects.filter(
            application_referral__destination_user=self.request.user,
            application_referral__is_enabled=True,
        ).distinct()


class AdminExportReferralApplicationListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    ordering_fields = ["create_at"]
    filterset_class = ApplicationListFilter

    def get_queryset(self):
        return ApplicationModel.objects.filter(
            application_referral__destination_user=self.request.user,
            application_referral__is_enabled=True,
        ).distinct()

    def get(self, *args, **kwargs):
        resource_class = AdminApplicationExportResource(user=self.request.user)
        dataset = resource_class.export(self.get_queryset())

        response = HttpResponse(dataset.xlsx, content_type="text/xlsx")
        response["Content-Disposition"] = 'attachment; filename="export_orders.xlsx"'
        return response


class AdminDetailApplicationView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminDetailApplicationSerializer
    lookup_field = "pk"

    def get_queryset(self):
        if self.request.user.is_superuser is True or self.request.user.is_admin is True:
            return (
                ApplicationModel.objects.all()
                .exclude(status=ApplicationModel.ApplicationStatusOptions.Not_Completed)
                .distinct()
            )
        else:
            return (
                ApplicationModel.objects.filter(
                    application_referral__destination_user=self.request.user
                )
                .exclude(status=ApplicationModel.ApplicationStatusOptions.Not_Completed)
                .distinct()
            )


class AdminDeleteApplicationView(generics.DestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    lookup_field = "pk"

    def get_queryset(self):
        return (
            ApplicationModel.objects.all()
            .exclude(status=ApplicationModel.ApplicationStatusOptions.Not_Completed)
            .distinct()
        )


class AdminUpdateApplicationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminUpdateApplicationSerializer
    lookup_field = "pk"

    def get_queryset(self):
        if self.request.user.is_superuser is True or self.request.user.is_admin is True:
            return ApplicationModel.objects.all().exclude(
                status=ApplicationModel.ApplicationStatusOptions.Not_Completed
            )
        else:
            user_faculty = (
                AdminModel.objects.filter(
                    user=self.request.user,
                    role=AdminModel.AdminRoleOptions.faculty_director,
                )
                .values_list("faculties_id", flat=True)
                .distinct()
            )
            return ApplicationModel.objects.filter(
                faculty__in=list(user_faculty),
                application_referral__destination_user=self.request.user,
            ).exclude(status=ApplicationModel.ApplicationStatusOptions.Not_Completed)


class AdminSubmitApplicationLetterView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        CanIssuanceLetterPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminSubmitApplicationLetterSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=self.request.data)
        ser.is_valid(raise_exception=True)
        return response.Response(ser.validated_data)
