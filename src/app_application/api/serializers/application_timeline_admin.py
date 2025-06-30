from django.db.models import Q

from rest_framework import serializers, exceptions

from app_application.models import TimeLineModel, ApplicationModel
from app_admin.models import AdminModel

from utils.base_errors import BaseErrors


class AdminApplicationTimeLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLineModel
        fields = ("id", "status", "message", "application", "jalali_created_at")
        extra_kwargs = {
            "id": {"read_only": True},
            "jalali_created_at": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user

    def validate(self, attrs):
        if (
            attrs["application"].status
            == ApplicationModel.ApplicationStatusOptions.Current
        ):
            user_role = self.user.user_admin.filter(
                Q(faculties=attrs["application"].faculty)
                & Q(role=AdminModel.AdminRoleOptions.faculty_director)
                | Q(fields=attrs["application"].field_of_study)
            ).first()
            if self.user.is_superuser is True or user_role is not None:
                return attrs
            else:
                raise exceptions.ParseError(
                    BaseErrors.user_do_not_have_permission_for_application
                )
        else:
            raise exceptions.ParseError(BaseErrors.cant_create_comment_for_application)

    def create(self, validated_data):
        return TimeLineModel.objects.create(user=self.user, **validated_data)
