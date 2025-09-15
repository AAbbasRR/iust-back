from .high_school import HighSchoolDetailUpdateView
from .bachelor_degree import BachelorDegreeDetailUpdateView
from .master_degree import MasterDegreeDetailUpdateView
from .faculty_admin import AdminFacultyListCreateView, AdminFacultyUpdateDeleteView, AdminFacultyListAllByDegreeView
from .faculty import FacultyListByDegreeView, FacultyListView
from .field_of_study_admin import (
    AdminFieldOfStudyListCreateView,
    AdminFieldOfStudyUpdateDeleteView,
)
from .groups_admin import AdminFacultyGroupsListCreateView, AdminFacultyGroupsUpdateDeleteView
