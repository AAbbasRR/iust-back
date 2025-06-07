from .application import (
    ListAllApplicationsView,
    ApplicationCreateView,
    ApplicationDetailUpdateView,
    ApplicationDeleteView,
)
from .application_admin import (
    AdminAllApplicationView,
    AdminExportApplicationListView,
    AdminDetailApplicationView,
    AdminDeleteApplicationView,
    AdminUpdateApplicationView,
    AdminReferralApplicationListView,
    AdminExportReferralApplicationListView,
    AdminSubmitApplicationLetterView,
)
from .application_timeline_admin import AdminCreateApplicationTimeLineView
from .documents import DocumentsCreateView, DocumentsDetailUpdateView
from .referral_admin import AdminCreateReferralAPIView
