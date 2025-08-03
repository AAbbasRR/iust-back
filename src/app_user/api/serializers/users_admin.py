from rest_framework import serializers, exceptions

from app_user.models import UserModel


class AdminUserListSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField("get_profile")
    applications_count = serializers.SerializerMethodField("get_applications_count")

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
            "is_active",
            "formatted_date_joined",
            "formatted_last_login",
            "profile",
            "applications_count"
        )

    def __init__(self, *args, **kwargs):
        super(AdminUserListSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user

    def get_applications_count(self, obj):
        return obj.user_application.count(),

    def get_profile(self, obj):
        return {
            "id": obj.user_profile.id,
            "phone_number": obj.user_profile.phone_number,
            "first_name": obj.user_profile.first_name,
            "last_name": obj.user_profile.last_name,
            "birth_date": obj.user_profile.birth_date,
            "gender": obj.user_profile.gender,
            "nationality": obj.user_profile.nationality,
            "passport_number": obj.user_profile.passport_number,
        }
