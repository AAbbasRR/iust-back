from rest_framework import generics, status, response

from utils import BaseVersioning
from utils.permissions import IsAuthenticatedPermission


class UserProfileDetailView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning

    def get(self, *args, **kwargs):
        user = self.request.user
        user_profile = user.user_profile
        address = user.user_address
        high_school = user.user_high_school
        complete = 0
        if user_profile.phone_number is not None:
            complete += 1
        if user_profile.first_name is not None:
            complete += 1
        if user_profile.last_name is not None:
            complete += 1
        if user_profile.birth_date is not None:
            complete += 1
        if user_profile.nationality is not None:
            complete += 1
        if user_profile.mother_language is not None:
            complete += 1
        if user_profile.other_languages is not None:
            complete += 1
        if user_profile.profile is not None:
            complete += 1
        if address.country is not None:
            complete += 1
        if address.city is not None:
            complete += 1
        if address.postal_code is not None:
            complete += 1
        if address.address is not None:
            complete += 1
        if high_school.country is not None:
            complete += 1
        if high_school.city is not None:
            complete += 1
        if high_school.date_of_graduation is not None:
            complete += 1
        if high_school.gpa is not None:
            complete += 1
        if high_school.field_of_study is not None:
            complete += 1
        user_applications = user.user_application.all()
        agent_applications = user.agent_applications.all()
        all_applications = user_applications.union(agent_applications)
        number_of_all_applications = all_applications.count()
        have_notification = user.user_notifications.filter(view_status=False).exists()
        return response.Response(
            {
                "full_name": f"{user_profile.first_name} {user_profile.last_name}",
                "profile_url": user_profile.profile_url(self.request),
                "number_applications": number_of_all_applications,
                "notification": have_notification,
                "complete_percent": (complete / 17) * 100,
            },
            status=status.HTTP_200_OK,
        )
