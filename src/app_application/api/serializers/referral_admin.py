from django.db.models import Q

from rest_framework import serializers, exceptions

from app_admin.models import AdminModel
from app_application.models import ReferralModel, TimeLineModel
from app_user.models import UserModel

from utils.base_errors import BaseErrors


class AdminCreateReferralSerializer(serializers.ModelSerializer):
    destination_users = serializers.ListField(
        child=serializers.IntegerField(), required=True, write_only=True
    )

    class Meta:
        model = ReferralModel
        fields = ("application", "destination_users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.method in ["PUT", "PATCH"]:
                for field_name, field in self.fields.items():
                    field.required = False

    def validate_destination_users(self, value):
        return UserModel.objects.filter(is_staff=True, pk__in=value).exclude(
            id=self.user.id
        )

    def validate(self, attrs):
        destination_users = attrs["destination_users"].filter(
            Q(user_admin__faculties=attrs["application"].faculty) | Q(is_superuser=True)
        )
        message = "ارجاع به "
        if self.user.is_superuser is True:
            for index, user in enumerate(destination_users):
                if index + 1 == len(destination_users):
                    message = message + f"{user.get_full_name()}"
                else:
                    message = message + f"{user.get_full_name()} - "
                ReferralModel.objects.create(
                    origin_user=self.user,
                    application=attrs["application"],
                    destination_user=user,
                )
            TimeLineModel.objects.create(
                application=attrs["application"],
                user=self.user,
                status=TimeLineModel.TimeLineStatusOptions.Referral,
                message=message,
            )
        else:
            user_faculty_role = self.user.user_admin.filter(
                role=AdminModel.AdminRoleOptions.faculty_director,
                faculties=attrs["application"].faculty,
            ).first()
            if user_faculty_role is not None:
                for index, user in enumerate(destination_users):
                    if index + 1 == len(destination_users):
                        message = message + f"{user.get_full_name()}"
                    else:
                        message = message + f"{user.get_full_name()} - "
                    ReferralModel.objects.create(
                        origin_user=self.user,
                        application=attrs["application"],
                        destination_user=user,
                    )
                TimeLineModel.objects.create(
                    application=attrs["application"],
                    user=self.user,
                    status=TimeLineModel.TimeLineStatusOptions.Referral,
                    message=message,
                )
            else:
                user_head_role = self.user.user_admin.filter(
                    role=AdminModel.AdminRoleOptions.department_head,
                    faculties=attrs["application"].faculty,
                    fields=attrs["application"].field_of_study,
                ).first()
                if user_head_role is not None:
                    destination_users = attrs["destination_users"].filter(
                        user_admin__faculties=attrs["application"].faculty
                    )
                    for index, user in enumerate(destination_users):
                        if index + 1 == len(destination_users):
                            message = message + f"{user.get_full_name()}"
                        else:
                            message = message + f"{user.get_full_name()} - "
                        ReferralModel.objects.create(
                            origin_user=self.user,
                            application=attrs["application"],
                            destination_user=user,
                        )
                    TimeLineModel.objects.create(
                        application=attrs["application"],
                        user=self.user,
                        status=TimeLineModel.TimeLineStatusOptions.Referral,
                        message=message,
                    )
                else:
                    raise exceptions.ParseError(
                        BaseErrors.user_do_not_have_role_for_referral
                    )

        return True
