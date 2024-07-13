from rest_framework import serializers

from app_education.models import HighSchoolModel
from app_user.models import UserModel


class HighSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighSchoolModel
        fields = (
            "id",
            "country",
            "city",
            "date_of_graduation",
            "gpa",
            "field_of_study",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "country": {"required": True, "allow_null": False},
            "city": {"required": True, "allow_null": False},
            "date_of_graduation": {"required": True, "allow_null": False},
            "gpa": {"required": True},
            "field_of_study": {
                "required": True,
                "allow_null": False,
            },
        }

    def __init__(self, *args, **kwargs):
        super(HighSchoolSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            try:
                if self.user.is_agent:
                    self.fields["email"] = serializers.EmailField(
                        required=True, write_only=True
                    )
            except Exception:
                pass

    def update(self, instance, validated_data):
        if self.user.is_agent:
            user_email = validated_data.pop("email")
            user = UserModel.objects.filter(email=user_email).first()
            if user is None:
                user = UserModel.objects.create_user_with_pass(
                    email=user_email, password=self.user.password
                )
            instance = user.user_high_school
        for field_name in validated_data:  # update high school fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
