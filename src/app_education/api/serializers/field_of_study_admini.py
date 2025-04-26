from rest_framework import serializers

from app_education.models import FieldOfStudyModel


class AdminFieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudyModel
        fields = (
            "id",
            "fa_name",
            "en_name",
            "ar_name",
            "is_active",
            "faculty",
            "requires_an_interview",
            "max_members",
        )
