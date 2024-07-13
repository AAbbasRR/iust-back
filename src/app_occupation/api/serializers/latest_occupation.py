from rest_framework import serializers

from app_occupation.models import LatestOccupationModel
from app_user.models import UserModel


class LatestOccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestOccupationModel
        fields = (
            "id",
            "occupation",
            "organization",
            "from_date",
            "to_date",
            "country",
            "city",
            "description",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "occupation": {"required": True},
            "organization": {"required": True},
            "from_date": {"required": True},
            "to_date": {"required": True},
            "country": {"required": True},
            "city": {"required": True},
            "description": {"required": False},
        }

    def __init__(self, *args, **kwargs):
        super(LatestOccupationSerializer, self).__init__(*args, **kwargs)
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
            instance = user.user_latest_occupation
        for field_name in validated_data:  # update latest occupation fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
