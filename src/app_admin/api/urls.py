from django.urls import path

from .views import *

app_name = "app_admin"
urlpatterns = [
    # login
    path("login/", AdminLoginView.as_view(), name="admin_login"),
    path("oauth/", AdminOauthLoginAPIView.as_view(), name="admin_oauth_login"),
    # staffs
    path("staffs/list/", AdminStaffsListAPIView.as_view(), name="admin_list_staffs"),
    path(
        "staffs/create_rule/",
        AdminStaffsCreateAPIView.as_view(),
        name="admin_create_rule_staff",
    ),
    path(
        "staffs/update_detele_rule/<int:pk>/",
        AdminStaffsUpdateDeleteAPIView.as_view(),
        name="admin_update_delete_rule_staff",
    ),
    # report
    path(
        "report/countries/",
        AdminCountryRequestsCountAPIView.as_view(),
        name="admin_countries_report",
    ),
    path(
        "report/applications/",
        AdminReportApplicationsAPIView.as_view(),
        name="admin_applications_report",
    ),
    path(
        "report/diffrent/",
        AdminReportDiffrentBarAPIView.as_view(),
        name="admin_diffrent_report",
    ),
    path(
        "report/hieatmap/",
        AdminReportHitMapAPIView.as_view(),
        name="admin_heatmap_report",
    ),
    path(
        "report/choropleth/",
        AdminReportCountryAPIView.as_view(),
        name="admin_choropleth_report",
    ),
    path(
        "report/barchart/",
        AdminReportBarChartAPIView.as_view(),
        name="admin_barchart_report",
    ),
    path(
        "report/averagetimeline/",
        AdminReportAverageReviewTimeAPIView.as_view(),
        name="admin_average_timeline_report",
    ),
    path(
        "settings/admin_list_settings/",
        AdminSettingsView.as_view(),
        name="admin_list_settings",
    ),
    path(
        "settings/admin_update_setting/",
        AdminUpdateView.as_view(),
        name="admin_update_setting",
    ),
]
