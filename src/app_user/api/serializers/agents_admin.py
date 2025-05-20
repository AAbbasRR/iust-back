from rest_framework import serializers

from app_user.models import UserModel


class AdminAgentsListSerializers(serializers.ModelSerializer):
    count_applications = serializers.SerializerMethodField(
        "get_count_applications", read_only=True
    )

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
            "password",
            "formatted_date_joined",
            "count_applications",
            "locked",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "formatted_date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        return UserModel.objects.create_user(
            **validated_data, is_active=True, is_agent=True, locked=False
        )

    def get_count_applications(self, obj):
        return obj.agent_applications.count()

    def update(self, instance, validated_data):
        for field_name in validated_data:  # update agent fields
            if field_name == "password":
                instance.change_password(validated_data[field_name])
            else:
                setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
