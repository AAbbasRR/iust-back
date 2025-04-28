from rest_framework import serializers

from app_admin.models import SettingsModel


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = (
            "id",
            "fa_signup_terms",
            "en_signup_terms",
            "ar_signup_terms",
            "fa_before_sign_text",
            "en_before_sign_text",
            "ar_before_sign_text",
            "fa_before_new_application_text",
            "en_before_new_application_text",
            "ar_before_new_application_text",
            "admin_application_text",
            "start_application_date",
            "end_application_date",
        )
        extra_kwargs = {
            "fa_signup_terms": {"read_only": False},
            "en_signup_terms": {"read_only": False},
            "ar_signup_terms": {"read_only": False},
            "fa_before_sign_text": {"read_only": False},
            "en_before_sign_text": {"read_only": False},
            "ar_before_sign_text": {"read_only": False},
            "fa_before_new_application_text": {"read_only": False},
            "en_before_new_application_text": {"read_only": False},
            "ar_before_new_application_text": {"read_only": False},
            "admin_application_text": {"read_only": False},
            "start_application_date": {"read_only": False},
            "end_application_date": {"read_only": False},
        }

