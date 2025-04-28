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

    def create(self, validated_data):
        return FieldOfStudyModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field_name in validated_data:  # update document fields
            setattr(instance, field_name, validated_data[field_name])
        instance.save()
        return instance
