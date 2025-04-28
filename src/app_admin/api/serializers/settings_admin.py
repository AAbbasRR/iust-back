from rest_framework import serializers

from app_admin.models import SettingsModel


class AdminSettingsSerializer(serializers.ModelSerializer):
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
            "fa_signup_terms": {"required": False},
            "en_signup_terms": {"required": False},
            "ar_signup_terms": {"required": False},
            "fa_before_sign_text": {"required": False},
            "en_before_sign_text": {"required": False},
            "ar_before_sign_text": {"required": False},
            "fa_before_new_application_text": {"required": False},
            "en_before_new_application_text": {"required": False},
            "ar_before_new_application_text": {"required": False},
            "admin_application_text": {"required": False},
            "start_application_date": {"required": False},
            "end_application_date": {"required": False},
        }

    def update(self, instance, validated_data):
        for field_name in validated_data:  # update document fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
