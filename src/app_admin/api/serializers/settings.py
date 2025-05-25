from rest_framework import serializers

from app_admin.models import SettingsModel


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = (
            "id",
            "start_register_date",
            "end_register_date",
        )
        extra_kwargs = {
            "start_register_date": {"read_only": False},
            "end_register_date": {"read_only": False},
        }
