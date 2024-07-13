from rest_framework import serializers

from app_education.models import BachelorDegreeModel
from app_user.models import UserModel


class BachelorDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BachelorDegreeModel
        fields = (
            "id",
            "country",
            "city",
            "date_of_graduation",
            "gpa",
            "field_of_study",
            "university",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "country": {"required": True, "allow_null": False, "allow_blank": False},
            "city": {"required": True, "allow_null": False, "allow_blank": False},
            "date_of_graduation": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
            "gpa": {"required": True},
            "field_of_study": {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
            },
            "university": {"required": True, "allow_null": False, "allow_blank": False},
        }

    def __init__(self, *args, **kwargs):
        super(BachelorDegreeSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user
            self.method = self.request.method
            if self.method in ["PUT", "PATCH"]:
                for field_name, field in self.fields.items():
                    field.required = False
            if self.user.is_agent:
                self.fields["email"] = serializers.EmailField(
                    required=True, write_only=True
                )

    def update(self, instance, validated_data):
        if self.user.is_agent:
            user_email = validated_data.pop("email")
            user = UserModel.objects.filter(email=user_email).first()
            if user is None:
                user = UserModel.objects.create_user_with_pass(
                    email=user_email, password=self.user.password
                )
            instance = user.user_bachelor_degree
        for field_name in validated_data:  # update bachelor degree fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
