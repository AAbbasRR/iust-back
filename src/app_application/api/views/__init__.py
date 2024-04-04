from .application import (
    ListAllApplicationsView,
    ApplicationCreateView,
    ApplicationDetailUpdateView,
)
from .application_admin import (
    AdminAllApplicationView,
    AdminExportApplicationListView,
    AdminDetailApplicationView,
    AdminUpdateApplicationView,
    AdminReferralApplicationListView,
    AdminExportReferralApplicationListView,
    AdminSubmitApplicationLetterView,
)
from .application_timeline_admin import AdminCreateApplicationTimeLineView
from .documents import DocumentsCreateView, DocumentsDetailUpdateView
from .referral_admin import AdminCreateReferralAPIView
