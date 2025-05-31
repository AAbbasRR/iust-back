from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from app_user.models import ProfileModel

import re

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField("get_profile_url")

    class Meta:
        model = ProfileModel
        fields = (
            "id",
            "phone_number",
            "iran_phone_number",
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "nationality",
            "passport_number",
            "mother_language",
            "other_languages",
            "english_status",
            "persian_status",
            "email",
            "profile",
            "profile_url",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"read_only": True},
            "phone_number": {"required": True},
            "iran_phone_number": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "first_name": {"required": True},
            "last_name": {"required": True},
            "birth_date": {"required": True},
            "gender": {"required": True, "allow_null": False, "allow_blank": False},
            "nationality": {"required": True},
            "passport_number": {"required": True},
            "mother_language": {"required": False},
            "other_languages": {"required": False},
            "english_status": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
            "persian_status": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
            "profile": {"required": False, "write_only": True},
            "profile_url": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.user.is_agent:
                self.fields["email"] = serializers.EmailField(
                    required=True, write_only=True
                )

    def validate_phone_number(self, value):
        pattern = r"^(?:\+|00)[1-9]\d{6,14}$"
        if not re.fullmatch(pattern, value):
            raise serializers.ValidationError(
                _("Invalid international phone number format.")
            )
        return value

    def to_internal_value(self, data):
        data = data.copy()
        if data.get("profile") == "null":
            data["profile"] = None
        return super().to_internal_value(data)

    def get_profile_url(self, obj):
        return obj.profile_url(self.request)

    def get_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        profile_obj = ProfileModel.objects.create(user=self.user, **validated_data)
        return profile_obj

    def update(self, instance, validated_data):
        if self.user.is_agent:
            user_email = validated_data.pop("email")
            user = UserModel.objects.find_by_email(email=user_email)
            if user is None:
                user = UserModel.objects.create_user_with_pass(
                    email=user_email, password=self.user.password
                )
            instance = user.user_profile
        for field_name in validated_data:  # update profile fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance


class ProfileInfoSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField("get_profile_url")

    class Meta:
        model = ProfileModel
        fields = (
            "id",
            "phone_number",
            "iran_phone_number",
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "nationality",
            "profile",
            "profile_url",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "phone_number": {"required": True},
            "iran_phone_number": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "first_name": {"required": True},
            "last_name": {"required": True},
            "birth_date": {"required": True},
            "gender": {"required": True, "allow_null": False, "allow_blank": False},
            "nationality": {"required": True},
            "profile": {"required": False, "write_only": True},
            "profile_url": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(ProfileInfoSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.user.is_agent:
                self.fields["email"] = serializers.EmailField(
                    required=True, write_only=True
                )

    def validate_phone_number(self, value):
        pattern = r"^(?:\+|00)[1-9]\d{6,14}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                _("Invalid international phone number format.")
            )
        return value

    def to_internal_value(self, data):
        data = data.copy()
        if data.get("profile") == "null":
            data["profile"] = None
        return super().to_internal_value(data)

    def get_profile_url(self, obj):
        return obj.profile_url(self.request)

    def create(self, validated_data):
        profile_obj = ProfileModel.objects.create(user=self.user, **validated_data)
        return profile_obj

    def update(self, instance, validated_data):
        for field_name in validated_data:  # update profile fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
