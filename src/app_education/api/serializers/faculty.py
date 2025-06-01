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
        fields = [
            "id",
            "fa_name",
            "en_name",
            "ar_name",
            "fields_of_studies",
        ]

    def get_fields_of_studies(self, obj):
        degree = self.context.get("degree")
        queryset = obj.fields_of_studies.all()

        if degree == "master":
            queryset = queryset.filter(master_active=True)
        elif degree == "phd":
            queryset = queryset.filter(phd_active=True)

        return FieldOfStudySerializer(queryset, many=True).data


class AllFacultySerializer(serializers.ModelSerializer):
    fields_of_studies = serializers.SerializerMethodField(
        "get_fields_of_studies", read_only=True
    )

    class Meta:
        model = FacultyModel
        fields = [
            "id",
            "fa_name",
            "en_name",
            "ar_name",
            "fields_of_studies",
        ]

    def get_fields_of_studies(self, obj):
        fields_of_studies = obj.fields_of_studies.all()
        return FieldOfStudySerializer(fields_of_studies, many=True).data
