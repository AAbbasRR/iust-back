from rest_framework import serializers

from app_education.models import FacultyModel

class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudyModel
        fields = ["id", "fa_name", "en_name", "ar_name"]

class AdminFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyModel
        fields = (
            "id",
            "fa_name",
            "en_name",
            "ar_name",
            "is_active",
        )

    def create(self, validated_data):
        return FacultyModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field_name in validated_data:  # update document fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance


class AdminFacultyByDegreeSerializer(serializers.ModelSerializer):
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

        if degree == "Master":
            queryset = queryset.all()
        elif degree == "P.H.D":
            queryset = queryset.all()

        return FieldOfStudySerializer(queryset, many=True).data