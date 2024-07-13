from django.contrib.auth import get_user_model

from rest_framework import serializers

from app_user.models import AddressModel

UserModel = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = (
            "id",
            "country",
            "city",
            "country_code",
            "postal_code",
            "city_code",
            "address",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "country": {"required": True},
            "city": {"required": True},
            "country_code": {"required": False},
            "postal_code": {"required": True},
            "city_code": {"required": False},
            "address": {"required": True},
        }

    def __init__(self, *args, **kwargs):
        super(AddressSerializer, self).__init__(*args, **kwargs)
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
            instance = user.user_address
        for field_name in validated_data:  # update address fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
