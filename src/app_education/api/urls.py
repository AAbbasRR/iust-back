from django.urls import path

from .views import *

app_name = "app_education"
urlpatterns = [
    path(
        "high_school/detail_update/",
        HighSchoolDetailUpdateView.as_view(),
        name="education_high_school_detail_update",
    ),
    path(
        "bachelor_degree/detail_update/",
        BachelorDegreeDetailUpdateView.as_view(),
        name="education_bachelor_degree_detail_update",
    ),
    path(
        "master_degree/detail_update/",
        MasterDegreeDetailUpdateView.as_view(),
        name="education_master_degree_detail_update",
    ),
    # Faculty
    path(
        "faculties/lists/",
        FacultyListView.as_view(),
        name="faculties_list_create",
    ),
    # Admin Faculty
    path(
        "admin/faculties/list_create/",
        AdminFacultyListCreateView.as_view(),
        name="admin_faculties_list_create",
    ),
    path(
        "admin/faculties/update_delete/<int:pk>/",
        AdminFacultyUpdateDeleteView.as_view(),
        name="admin_faculties_update_delete",
    ),
    # Admin Field Of Study
    path(
        "admin/field_of_study/list_create/",
        AdminFieldOfStudyListCreateView.as_view(),
        name="admin_field_of_study_list_create",
    ),
    path(
        "admin/field_of_study/update_delete/<int:pk>/",
        AdminFieldOfStudyUpdateDeleteView.as_view(),
        name="admin_field_of_study_update_delete",
    ),
# Admin Faculty Groups
    path(
        "admin/faculty_groups/list_create/",
        AdminFacultyGroupsListCreateView.as_view(),
        name="admin_faculty_groups_list_create",
    ),
    path(
        "admin/faculty_groups/update_delete/<int:pk>/",
        AdminFacultyUpdateDeleteView.as_view(),
        name="admin_faculty_groups_update_delete",
    ),
]
