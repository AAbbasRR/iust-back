from rest_framework import serializers

from app_admin.models import SettingsModel


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = (
            "id",
            "start_register_date",
            "end_register_date",
            "start_phd_register_date",
            "end_phd_register_date",
            "fa_terms",
            "en_terms",
            "ar_terms",
        )
        extra_kwargs = {
            "start_register_date": {"read_only": False},
            "end_register_date": {"read_only": False},
            "start_phd_register_date": {"read_only": False},
            "end_phd_register_date": {"read_only": False},
            "fa_terms": {"read_only": False},
            "en_terms": {"read_only": False},
            "ar_terms": {"read_only": False},
        }
