from django.urls import path

from .views import *

app_name = "app_application"
urlpatterns = [
    path("list/", ListAllApplicationsView.as_view(), name="application_all_list"),
    path("create/", ApplicationCreateView.as_view(), name="application_create"),
    path(
        "detail_update/<int:pk>/",
        ApplicationDetailUpdateView.as_view(),
        name="application_detail_update",
    ),
    path(
        "delete/<int:pk>/",
        ApplicationDeleteView.as_view(),
        name="application_delete",
    ),
    path(
        "document/create/",
        DocumentsCreateView.as_view(),
        name="application_create_document",
    ),
    path(
        "document/detail_update/<int:pk>/",
        DocumentsDetailUpdateView.as_view(),
        name="application_detail_update_document",
    ),
    # admin
    path(
        "admin/all-application/list/",
        AdminAllApplicationView.as_view(),
        name="admin_all_application_list",
    ),
    path(
        "admin/all-application/list/export/",
        AdminExportApplicationListView.as_view(),
        name="admin_export_all_application_list",
    ),
    path(
        "admin/referral-application/list/",
        AdminReferralApplicationListView.as_view(),
        name="admin_referral_application_list",
    ),
    path(
        "admin/referral-application/list/export/",
        AdminExportReferralApplicationListView.as_view(),
        name="admin_export_referral_application_list",
    ),
    path(
        "admin/all-application/detail/<int:pk>/",
        AdminDetailApplicationView.as_view(),
        name="admin_application_detail",
    ),
    path(
        "admin/all-application/delete/<int:pk>/",
        AdminDeleteApplicationView.as_view(),
        name="admin_application_delete",
    ),
    path(
        "admin/application/timeline/",
        AdminCreateApplicationTimeLineView.as_view(),
        name="admin_application_timeline_create",
    ),
    path(
        "admin/application/referral/create/",
        AdminCreateReferralAPIView.as_view(),
        name="admin_application_referral_create",
    ),
    path(
        "admin/application/update/<int:pk>/",
        AdminUpdateApplicationView.as_view(),
        name="admin_application_update_status",
    ),
    path(
        "admin/application/issuance_letter/",
        AdminSubmitApplicationLetterView.as_view(),
        name="admin_application_issuance_letter",
    ),
]
