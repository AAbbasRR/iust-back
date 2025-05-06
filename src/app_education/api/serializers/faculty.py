from rest_framework import serializers

from app_education.models import FacultyModel, FieldOfStudyModel


class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudyModel
        fields = ["id", "fa_name", "en_name", "ar_name"]


class FacultySerializer(serializers.ModelSerializer):
    fields_of_studies = serializers.SerializerMethodField(
        "get_fields_of_studies", read_only=True
    )

    class Meta:
        model = FacultyModel
        fields = ["id", "fa_name", "en_name", "ar_name", "degree", "fields_of_studies"]

    def get_fields_of_studies(self, obj):
        fields_of_studies = obj.fields_of_studies.filter(is_active=True)
        return FieldOfStudySerializer(fields_of_studies, many=True).data
