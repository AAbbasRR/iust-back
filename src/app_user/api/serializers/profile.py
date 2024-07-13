from django.contrib.auth import get_user_model

from rest_framework import serializers

from app_user.models import ProfileModel

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField("get_profile_url")

    class Meta:
        model = ProfileModel
        fields = (
            "id",
            "phone_number",
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
            "profile",
            "profile_url",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "phone_number": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "birth_date": {"required": True},
            "gender": {"required": True, "allow_null": False},
            "nationality": {"required": True},
            "passport_number": {"required": True},
            "mother_language": {"required": False},
            "other_languages": {"required": False},
            "english_status": {"required": True, "allow_null": False},
            "persian_status": {"required": True, "allow_null": False},
            "profile": {"required": True, "write_only": True},
            "profile_url": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.method in ["PUT"]:
                for field_name, field in self.fields.items():
                    field.required = False
            if self.user.is_agent:
                self.fields["email"] = serializers.EmailField(
                    required=True, write_only=True
                )

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
        if self.user.is_agent:
            user_email = validated_data.pop("email")
            user = UserModel.objects.filter(email=user_email).first()
            if user is None:
                user = UserModel.objects.create_user_with_pass(
                    email=user_email, password=self.user.password
                )
            instance = user.user_profile
        for field_name in validated_data:  # update profile fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
