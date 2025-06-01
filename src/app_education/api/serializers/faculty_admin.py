from rest_framework import serializers

from app_education.models import FacultyModel


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
