from rest_framework import serializers

from app_admin.models import SettingsModel


class AdminSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = (
            "id",
            "start_register_date",
            "end_register_date",
            "start_phd_register_date",
            "end_phd_register_date",
        )
        extra_kwargs = {
            "start_register_date": {"required": False},
            "end_register_date": {"required": False},
            "start_phd_register_date": {"required": False},
            "end_phd_register_date": {"required": False},
        }

    def update(self, instance, validated_data):
        for field_name in validated_data:  # update document fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
